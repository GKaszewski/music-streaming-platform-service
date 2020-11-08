from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField 
from model_utils import Choices

from  rest_framework import serializers

class User(AbstractUser):
    def __str__(self):
        return self.username

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    nickname = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.nickname

class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, default='')
    cover_url = models.URLField() # default = 'url to default cover'         

    def __str__(self):
        return '{} - {}'.format(self.name, self.artist.nickname)

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    song_url = models.URLField(null=True)
    name = models.CharField(max_length=50, default='')
    CATEGORIES = Choices('POP','INDIE','ROCK','RAP','HIP-HOP','ELECTRONIC','JAZZ', 'ROMANTIC','HAPPY','SAD')
    category = models.CharField(choices=CATEGORIES, max_length=50, default=CATEGORIES.SAD)

    def __str__(self):
        return '{} - {}'.format(str(self.artist), self.name)

class Playlist(models.Model):
    name = models.CharField(max_length=50)
    content = models.ManyToManyField(Song, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only' : True, 'required' : True},}

class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Artist
        fields = ('user', 'nickname', 'bio')
        ordering = ['-nickname']


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    class Meta:
        model = Album
        fields = '__all__'
        ordering = ['-artist__nickname', '-name']

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    album = AlbumSerializer()
    class Meta:
        model = Song
        fields = ('album', 'artist', 'song_url' ,'name', 'category')
        ordering = ['-artist__nickname', '-name']

class PlaylistSerializer(serializers.ModelSerializer):
    content = SongSerializer(many=True)
    author = UserSerializer()
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'content', 'author')
        ordering = ['-author__username', '-name']
        extra_kwargs = {'content': {'required': False}}



