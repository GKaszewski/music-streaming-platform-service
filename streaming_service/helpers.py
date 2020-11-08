from . import models

def add_content(data, content):
    for content_info in data:
            song = models.Song.objects.get(album__name=content_info['album'], artist__nickname=content_info['artist'], name=content_info['name'])
            content.append(song)