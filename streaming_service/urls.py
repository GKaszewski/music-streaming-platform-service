from django.urls import path
from django.conf.urls import include
from . import views, song_api

from rest_framework import routers

router = routers.DefaultRouter()
router.register('song', views.SongViewSet, base_name='song')
router.register('playlist', views.PlaylistViewSet, base_name='playlist')

urlpatterns = [
    path('', views.MarkdownIndex.as_view(), name='indexPage'),
    path('upload/song', views.UploadSongView.as_view(), name='uploadSong'),
    path('api/', include(router.urls), name='api'),
]