from rest_framework import serializers
from rest_framework import viewsets
from .models import Song, Playlist

class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('albumName', 'albumUrl', 'author', 'songUrl' ,'title', 'category')

class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    content = SongSerializer(many=True)
    class Meta:
        model = Playlist
        fields = ('name', 'content')