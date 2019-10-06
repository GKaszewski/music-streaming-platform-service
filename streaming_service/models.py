from django.db import models
from django.contrib.postgres.fields import ArrayField 
from model_utils import Choices

class Song(models.Model):
    albumName = models.CharField(max_length=100)
    albumUrl = models.URLField()
    author = models.CharField(max_length=200)
    songUrl = models.CharField(max_length=400)
    title = models.CharField(max_length=200)
    CATEGORIES = Choices('POP','INDIE','ROCK','RAP','HIP-HOP','ELECTRONIC','JAZZ''ROMANTIC','HAPPY','SAD')
    category = models.CharField(choices=CATEGORIES, max_length=50, default=CATEGORIES.SAD)

    def __str__(self):
        return self.author + ' ' + self.title

class Playlist(models.Model):
    name = models.CharField(max_length = 90)
    content = models.ManyToManyField(Song)

    def __str__(self):
        return self.name
