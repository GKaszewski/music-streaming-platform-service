from django.contrib import admin
from . import models


class SongAdminModel(admin.ModelAdmin):
    list_display = ('albumName', 'author', 'title', 'albumUrl', 'songUrl')
    list_filter = ('author', 'title', 'albumName')
    search_fields = ['author', 'title', 'albumName']

admin.site.register(models.Song, SongAdminModel)