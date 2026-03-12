from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            if request.user.is_superuser:
                return True
            return obj.owner == request.user
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Moderators').exists()
