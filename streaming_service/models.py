from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField 
from model_utils import Choices

from  rest_framework import serializers

class User(AbstractUser):
    avatar_url = models.URLField(blank=True, null=True)
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


class Follower(models.Model):
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_user')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower_user', 'following_user'], name='unique_followers')
        ]

        ordering = ['-created']

    def __str__(self):
        return "{} follows {}".format(self.follower_user.username, self.following_user.username)

class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class FollowingSerializer(serializers.ModelSerializer):
    following_user = PartialUserSerializer()
    class Meta:
        model = Follower
        fields = ('id', 'following_user', 'created')

class FollowersSerializer(serializers.ModelSerializer):
    follower_user = PartialUserSerializer()
    class Meta:
        model = Follower
        fields = ('id', 'follower_user', 'created')

class UserSerializer(serializers.ModelSerializer):
    following_user = serializers.SerializerMethodField()
    followers_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'avatar_url', 'following_user', 'followers_user')
        extra_kwargs = {'password': {'write_only' : True, 'required' : True},}

    def get_following_user(self, obj):
        return FollowingSerializer(obj.following_user.all(), many=True).data
    
    def get_followers_user(self, obj):
        return FollowersSerializer(obj.followers_user.all(), many=True).data

class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Artist
        fields = ('id', 'user', 'nickname', 'bio')
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
        fields = ('id', 'album', 'artist', 'song_url' ,'name', 'category')
        ordering = ['-artist__nickname', '-name']

class PlaylistSerializer(serializers.ModelSerializer):
    content = SongSerializer(many=True)
    author = UserSerializer()
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'content', 'author')
        ordering = ['-author__username', '-name']
        extra_kwargs = {'content': {'required': False}}


class UserFollowerSerializer(serializers.ModelSerializer):
    follower_user = PartialUserSerializer()
    following_user = PartialUserSerializer()

    class Meta:
        model = Follower
        fields = '__all__'