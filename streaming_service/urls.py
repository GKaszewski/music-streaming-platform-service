from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('songs', views.SongViewSet, basename='songs')
router.register('playlists', views.PlaylistViewSet, basename='playlists')
router.register('users', views.UserViewSet, basename='users')
router.register('artists', views.ArtistViewSet, basename='artists')

urlpatterns = [
    path('', views.MarkdownIndex.as_view(), name='indexPage'),
    path('auth/', views.AuthUserToken.as_view()),
    path('api/', include(router.urls), name='api'),
]