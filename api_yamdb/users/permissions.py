from rest_framework import permissions


class OwnerOrAdminOnly(permissions.BasePermission):
    '''Permission to only allow author of an object to edit it.'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin or 
            obj.author == request.user and
            view.action in ['retrieve', 'update']
        )
            
        
class SelfPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            view.action in ['retrieve', 'update']
        )