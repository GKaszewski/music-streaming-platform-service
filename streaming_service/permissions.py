from rest_framework import permissions
from .models import Artist

class IsOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
        


class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user_info = request.user
        artist = Artist.objects.filter(user__id=user_info.id).first()
        if artist:
            return True

        return False
        
