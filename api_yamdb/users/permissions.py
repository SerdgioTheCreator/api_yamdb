from rest_framework import permissions


class AdminOrMyselfOnly(permissions.BasePermission):
    '''
    Permission for users to alter their profile and admins to have full access.
    '''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
            or obj == request.user
            and view.action in ['retrieve', 'update']
        )


class AdminOrReadOnly(permissions.BasePermission):
    '''
    Permission read only for everyoneand admins to have full access.
    '''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_staff
        )


class AdminOrModerOrAuthor(permissions.BasePermission):
    '''
    Permission for users to control reviews or comments
    and admins or moderators to have full access.
    '''
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_staff
            or request.user.is_moderator
            or obj.author == request.user
            or request.user.is_authenticated and view.action == 'create'
        )
