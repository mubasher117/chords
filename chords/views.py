from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Song, PlaylistTrack, Playlist, PlayHistory
from django.db import transaction
import datetime


def index(request):  # the index view
    message = False
    songs = Song.objects.all()
    recentSongs = Song.objects.all().order_by('-uploaded_at')
    user_recommendation = []
    playlists = None
    songshistory = []
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
        message = True
        usersongshistory = PlayHistory.objects.filter(user=request.user)
        for history in usersongshistory:
            songshistory.append(history.song)
            genre = history.song.genre
            print(genre)
            for song in songs:
                if song.genre == genre and song != history.song:
                    user_recommendation.append(song)
    return render(request, "songs/index.html", {'recommendations': user_recommendation, 'playlists': playlists, 'message': message, 'recentSongs': recentSongs, 'usersongshistory': songshistory[::-1]})


def signup(request):
    user = User.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        print("in first condition")
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'songs/signup.html', {'form': form})


@staff_member_required
def uploadSong(request):
    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                song = Song.objects.get(tittle=form.tittle, album=form.album)
            except Song.DoesNotExist:
                song = None
            if song == None:
                form.save()
                form = UploadSongForm()
                return render(request, 'songs/uploadSong.html', {'Message': True, 'form': form})
    else:
        form = UploadSongForm()
    return render(request, 'songs/uploadSong.html', {'form': form})


def songs(request):
    randoms = Song.objects.all().order_by('?')
    random_songs = []
    random_songs.append(randoms[0])
    random_songs.append(randoms[1])
    random_songs.append(randoms[2])
    playlists = None
    user_recommendation = []
    songshistory = []
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
        usersongshistory = PlayHistory.objects.filter(user=request.user)

        for history in usersongshistory:
            songshistory.append(history.song)
            genre = history.song.genre
            print(genre)
            for song in randoms:
                if song.genre == genre and song != history.song:
                    user_recommendation.append(song)
    songs = Song.objects.all()
    print(len(user_recommendation))
    print(len(usersongshistory))
    return render(request, "songs/songs.html", {'songs': songs, 'playlists': playlists, 'random_songs': random_songs, 'recommendations': user_recommendation, 'usersongshistory': songshistory})


@login_required
def playlist(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "songs/playlists.html", {'playlists': playlists})


@login_required
def addToPlaylist(request, playlist, song):
    request.session['song_to_add'] = 'All is found'
    song1 = Song.objects.get(tittle=song)
    playlist1 = Playlist.objects.get(name=playlist)
    exist = False
    try:
        song = PlaylistTrack.objects.get(song=song1, playlist=playlist1)
    except PlaylistTrack.DoesNotExist:
        song = None
    if song == None:
        playlist1.tracks.add(song1)
    else:
        exist = True
    songs = Song.objects.all()
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "songs/songs.html", {'songs': songs, 'exist': exist, 'playlists': playlists})


@login_required
def createPlaylist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            try:
                playlist = Playlist.objects.get(name=form.cleaned_data['name'])
            except Playlist.DoesNotExist:
                playlist = None
            if playlist == None:
                playlist = form.save(commit=False)
                playlist.user = request.user
                playlist.save()
            playlists = Playlist.objects.filter(user=request.user)
            return render(request, "songs/playlists.html", {'playlists': playlists})
    else:
        print("IN ELSE")
        form = PlaylistForm()
    return render(request, 'songs/createPlaylist.html', {'form': form})


@login_required
def deleteSong(request, playlist, song):
    song1 = Song.objects.get(tittle=song)
    playlist1 = Playlist.objects.get(name=playlist)
    playlist1.tracks.remove(song1)
    songs = playlist1.tracks.all()
    count = playlist1.tracks.all().count()
    if count != 0:
        song = songs[0]
    return render(request, "songs/playSong.html", {'currentSong': song, 'songs': songs, 'name': playlist1.name, 'type1': 'playlist'})


@login_required
def deletePlaylist(request, playlist):
    playlist1 = Playlist.objects.filter(name=playlist).delete()
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, "songs/playlists.html", {'playlists': playlists})


@login_required
def playSong(request, type1, songName):
    song = None
    if type1 == 'song':
        songs = Song.objects.all()
        song = Song.objects.get(tittle=songName)
        print(song.genre)
    elif type1 == 'playlist':
        playlist = Playlist.objects.get(name=songName)
        count = playlist.tracks.all().count()
        songs = playlist.tracks.all()

        if count != 0:
            song = songs[0]
    elif type1 == "genre":
        songs = Song.objects.filter(genre=songName)
        count = Song.objects.filter(genre=songName).count()
        if count != 0:
            song = songs[0]
    try:
        songhistory = PlayHistory.objects.get(song=song, user=request.user)
    except PlayHistory.DoesNotExist:
        songhistory = None
    if song != None:
        if songhistory == None:
            PlayHistory.objects.create(user=request.user, song=song)
        else:
            songhistory.played_on = datetime.datetime.now()
    randoms = Song.objects.all().order_by('?')
    user_recommendation = []
    songshistory = []
    if request.user.is_authenticated:
        usersongshistory = PlayHistory.objects.filter(user=request.user)

        for history in usersongshistory:
            songshistory.append(history.song)
            genre = history.song.genre
            print(genre)
            for song1 in randoms:
                if song1.genre == genre and song1 != history.song:
                    user_recommendation.append(song1)
        user_recommendation = []
        last_played_song = usersongshistory[len(usersongshistory)-1].song
        print(last_played_song.tittle)
        print(song.tittle)
        for song2 in randoms:
            if song2.genre == song.genre and song2.tittle != song.tittle:
                user_recommendation.append(song2)

    print(len(user_recommendation))
    print(len(usersongshistory))
    return render(request, "songs/playSong.html", {'currentSong': song, 'songs': songs, 'name': songName, 'type1': type1, 'recommendations': user_recommendation, 'usersongshistory': songshistory[::-1]})

    def page_not_found(request):
        return render(request, "songs/404.html",)
