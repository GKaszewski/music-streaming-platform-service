from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('songs', views.SongViewSet, basename='songs')
router.register('playlists', views.PlaylistViewSet, basename='playlists')

urlpatterns = [
    path('', views.MarkdownIndex.as_view(), name='indexPage'),
    path('auth/', views.AuthUserToken.as_view()),
    #path('upload/song', views.UploadSongView.as_view(), name='uploadSong'),
    url(r'^api/users/register/$', views.CreateUserViewSet.as_view()),
    url(r'^api/users/$', views.UserViewSet.as_view()),
    path('api/', include(router.urls), name='api'),
]