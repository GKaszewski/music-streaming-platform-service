from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from rest_framework import viewsets
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