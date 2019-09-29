from rest_framework import serializers
from rest_framework import viewsets
from .models import Song

class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('albumName', 'albumUrl', 'author', 'songUrl' ,'title')

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer