from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from rest_framework import viewsets, filters, permissions, status, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models

import os

from microservice import settings

def index(request):
    return HttpResponse('<b>This is api page</b>')

class MarkdownIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        markdown_text = open(os.path.join(settings.TEMPLATES_DIR, 'readme.md')).read()

        context = super(MarkdownIndex, self).get_context_data(**kwargs)
        context['markdowntext'] = markdown_text

        return context

class SongViewSet(viewsets.ModelViewSet):
    search_fields = ['author', 'title', 'albumName', 'category']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Song.objects.all()
    serializer_class = models.SongSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.IsAdminUser,)

        return super(SongViewSet, self).get_permissions()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
class PlaylistViewSet(viewsets.ModelViewSet):
    search_fields = ['name', 'author',]
    filter_backends = (filters.SearchFilter,)
    queryset = models.Playlist.objects.all()
    serializer_class = models.PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    
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
            self.permission_classes = (permissions.IsAdminUser,)

        return super(UserViewSet, self).get_permissions()

    
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