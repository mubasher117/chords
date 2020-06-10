"""Chord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path 
from chords import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
  
urlpatterns = [ 
    path('', views.index, name = 'home'),  
    path('signup', views.signup, name='signup'),  
    path('login', auth_views.LoginView.as_view(template_name='songs/login.html'),  name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='songs/login.html'), name="logout"), 
    path('song', views.songs, name='songs'),  
    path('playlist', views.playlist, name='playlist'),  
    path('addToPlaylist/<playlist>/<song>', views.addToPlaylist, name='addToPlaylist'),  
    path('deletePlaylist/<playlist>', views.deletePlaylist, name = 'deletePlaylist'),
    path('createPlaylist', views.createPlaylist, name = 'createPlaylist'),
    path('admin/', admin.site.urls),
    path('uploadSong', views.uploadSong, name = 'uploadSong'),
    path('deleteSong/<playlist>/<song>', views.deleteSong, name = 'deleteSong'),
    path('playSong/<type1>/<songName>', views.playSong, name = 'playSong') 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

