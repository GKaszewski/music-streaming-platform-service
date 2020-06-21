from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField 
from model_utils import Choices

from  rest_framework import serializers

class Song(models.Model):
    albumName = models.CharField(max_length=100)
    albumUrl = models.URLField()
    author = models.CharField(max_length=200)
    songUrl = models.CharField(max_length=400)
    title = models.CharField(max_length=200)
    CATEGORIES = Choices('POP','INDIE','ROCK','RAP','HIP-HOP','ELECTRONIC','JAZZ', 'ROMANTIC','HAPPY','SAD')
    category = models.CharField(choices=CATEGORIES, max_length=50, default=CATEGORIES.SAD)

    def __str__(self):
        return self.author + ' ' + self.title

class Playlist(models.Model):
    name = models.CharField(max_length = 90)
    content = models.ManyToManyField(Song)

    def __str__(self):
        return self.name

class User(AbstractUser):
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.username

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('albumName', 'albumUrl', 'author', 'songUrl' ,'title', 'category')

class PlaylistSerializer(serializers.ModelSerializer):
    content = SongSerializer(many=True)
    class Meta:
        model = Playlist
        fields = ('name', 'content')

class UserSerializer(serializers.ModelSerializer):
    playlists = PlaylistSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'playlists', 'password')
        extra_kwargs = {'password': {'write_only' : True, 'required' : True},}

