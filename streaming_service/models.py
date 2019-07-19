from django.db import models

class Song(models.Model):
    albumName = models.CharField(max_length=100)
    albumUrl = models.URLField()
    author = models.CharField(max_length=200)
    songUrl = models.URLField()
    title = models.CharField(max_length=200)

