from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from rest_framework import viewsets, filters, permissions, status, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models, helpers
from .permissions import IsOwnProfile, IsArtist
import os

from microservice import settings
class MarkdownIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        markdown_text = open(os.path.join(settings.TEMPLATES_DIR, 'readme.md')).read()

        context = super(MarkdownIndex, self).get_context_data(**kwargs)
        context['markdowntext'] = markdown_text

        return context

class SongViewSet(viewsets.ModelViewSet):
    search_fields = ['artist__nickname', 'name', 'album__name', 'category']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Song.objects.all().order_by('album__name')
    serializer_class = models.SongSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnProfile, IsArtist)

    def create(self, request, *args, **kwargs):
        artist = models.Artist.objects.get(user=request.user)
        album, created = models.Album.objects.get_or_create(name=request.data['album_name'], cover_url=request.data['cover_url'], artist=artist)
        new_song = models.Song.objects.create(album=album, artist=artist, song_url=request.data['song_url'], name=request.data['name'],category=request.data['category'])
        serializer = models.SongSerializer(new_song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PlaylistViewSet(viewsets.ModelViewSet):
    search_fields = ['name', 'author',]
    filter_backends = (filters.SearchFilter,)
    queryset = models.Playlist.objects.all()
    serializer_class = models.PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        user = request.user
        name = request.data['name']
        content_data = request.data['content']
        content = []
        helpers.add_content(content_data, content)
        new_playlist, created = models.Playlist.objects.get_or_create(name=name, author=user)
        if not created:
            return Response('Already exists!',status=status.HTTP_403_FORBIDDEN)
        new_playlist.content.set(content)
        new_playlist.save()
        serializer = models.PlaylistSerializer(new_playlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def put(self, request, *args, **kwargs):
        user = request.user
        name = request.data['name']
        content_data = request.data['content']
        content = []
        helpers.add_content(content_data, content)
        playlist = models.Playlist.objects.get(name=name, author=user)
        playlist.content.set(content)
        playlist.save()
        serializer = models.PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        playlist = models.Playlist.objects.filter(name=request.data['name'], author=request.user).first()
        if not playlist:
            return Response("Couldn't find.",status=status.HTTP_404_NOT_FOUND)
        playlist.delete()
        return Response('Deleted!', status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = models.UserSerializer
    queryset = models.User.objects.all()
    lookup_field = 'username'
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = models.User.objects.create_user(**data)
        user.save()
        return Response(data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
        if self.request.method == 'DELETE':
            self.permission_classes = (permissions.IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()


class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = models.ArtistSerializer
    queryset = models.Artist.objects.all().order_by('nickname')
    lookup_field = 'nickname'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnProfile, )

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)

        return super(ArtistViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        raw_user_data = {'username':request.data['username'], 'password':request.data['password']}
        user_serializer = models.UserSerializer(data=raw_user_data, context={'request': request})
        user_serializer.is_valid(raise_exception=True)
        user_data = user_serializer.validated_data
        user = models.User.objects.create_user(**user_data)
        user.save()
        artist = models.Artist.objects.create(user=user, nickname=request.data['nickname'], bio=request.data['bio'])
        artist_serializer = models.ArtistSerializer(artist)
        artist_data = artist_serializer.data
        return Response(artist_data, status=status.HTTP_201_CREATED)

    
class AuthUserToken(ObtainAuthToken):
    permissions_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = models.UserSerializer(user, many=False)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user_serializer.data,
        })