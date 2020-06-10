from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username',
                  'email', 'password1', 'password2']

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('tittle', 'album', 'genre', 'image', 'songFile')

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('name',)
class PlayListTrackForm(forms.ModelForm):
    class Meta:
        model = PlaylistTrack
        fields = ('playlist', 'song',)

class PlayHistoryForm(forms.ModelForm):
    class Meta:
        model = PlayHistory
        fields = ('user', 'song',)
