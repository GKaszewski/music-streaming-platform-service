from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from rest_framework import viewsets, permissions, filters, generics
from . import models, song_api

import os

from microservice import settings

# Create your views here.

def index(request):
    return HttpResponse('<b>This is api page</b>')

class MarkdownIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        markdown_text = open(os.path.join(settings.TEMPLATES_DIR, 'readme.md')).read()

        context = super(MarkdownIndex, self).get_context_data(**kwargs)
        context['markdowntext'] = markdown_text

        return context

class UploadSongView(TemplateView):
    template_name = 'songForm.html'

class SongViewSet(viewsets.ModelViewSet):
    search_fields = ['author', 'title', 'albumName', 'category']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Song.objects.all()
    serializer_class = song_api.SongSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PlaylistViewSet(viewsets.ModelViewSet):
    search_fields = ['name',]
    filter_backends = (filters.SearchFilter,)
    queryset = models.Playlist.objects.all()
    serializer_class = song_api.PlaylistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)