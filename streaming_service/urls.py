from django.urls import path
from django.conf.urls import include
from . import views, song_api

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'song/get', song_api.SongViewSet, base_name='getSongs')

urlpatterns = [
    path('', views.MarkdownIndex.as_view(), name='indexPage'),
    path('upload/song', views.UploadSongView.as_view(), name='uploadSong'),
    path('api/', include(router.urls), name='api')
]