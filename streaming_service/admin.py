from django.contrib import admin
from . import models
from rest_framework.authtoken.admin import TokenAdmin

class SongAdminModel(admin.ModelAdmin):
    list_display = ('albumName', 'author', 'title', 'albumUrl', 'songUrl')
    list_filter = ('author', 'title', 'albumName')
    search_fields = ['author', 'title', 'albumName']

TokenAdmin.raw_id_fields = ['user']

admin.site.register(models.Song, SongAdminModel)
admin.site.register(models.User)
admin.site.register(models.Playlist)