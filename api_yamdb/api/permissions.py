from rest_framework import permissions


class AdminOrMyselfOnly(permissions.BasePermission):
    '''
    Permission for users to alter their profile and admins to have full access.
    '''
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    '''
    Permission read only for everyoneand admins to have full access.
    '''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class AdminOrModeratorOrAuthor(permissions.IsAuthenticatedOrReadOnly):
    '''
    Permission for users to control reviews or comments
    and admins or moderators to have full access.
    '''
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        )
