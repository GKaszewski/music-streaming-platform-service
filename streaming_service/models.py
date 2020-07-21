from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField 
from model_utils import Choices

from  rest_framework import serializers

class User(AbstractUser):
    def __str__(self):
        return self.username

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
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only' : True, 'required' : True},}

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('albumName', 'albumUrl', 'author', 'songUrl' ,'title', 'category')

class PlaylistSerializer(serializers.ModelSerializer):
    content = SongSerializer(many=True)
    author = UserSerializer()
    class Meta:
        model = Playlist
        fields = ('name', 'content', 'author')



