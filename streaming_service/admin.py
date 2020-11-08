from django.contrib import admin
from . import models
from rest_framework.authtoken.admin import TokenAdmin

class SongAdminModel(admin.ModelAdmin):
    list_display = ('album', 'artist', 'name', 'song_url')
    list_filter = ('album', 'artist', 'name', 'song_url')
    search_fields = ['album', 'artist', 'name', 'song_url']

TokenAdmin.raw_id_fields = ['user']

admin.site.register(models.Song, SongAdminModel)
admin.site.register(models.User)
admin.site.register(models.Artist)
admin.site.register(models.Album)
admin.site.register(models.Playlist)