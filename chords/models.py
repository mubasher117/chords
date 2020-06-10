from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

ROCK = 'RCK'
HIP_HOP = 'HH'


class Song(models.Model):
    GENRES = [
        ('Rock','Rock'),
        ('Hip Hop','Hip Hop'), 
        ('Blues', 'blues'), 
        ('Heavy Metal', 'Heavy Metal'), 
        ('Classical', 'Classical'), 
        ('Funk', 'Funk')]
    id = models.IntegerField(primary_key=True)
    tittle = models.CharField(max_length=255)
    album = models.CharField(max_length=255, null = True, blank = True)
    genre = models.CharField(max_length = 30, choices=GENRES)
    image = models.ImageField(upload_to='images/', blank = True , null = True)
    songFile = models.FileField(upload_to='musics/', help_text=("Allowed type - .mp3, .wav, .ogg"))
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.tittle

class Playlist(models.Model):
    name = models.CharField(max_length = 50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tracks = models.ManyToManyField('Song', through='PlaylistTrack')

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete = models.CASCADE)
    song =    models.ForeignKey(Song, on_delete = models.CASCADE)

class PlayHistory(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    song = models.ForeignKey(Song, on_delete = models.CASCADE)
    played_on = models.DateTimeField(auto_now_add=True)

