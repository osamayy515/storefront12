from rest_framework import permissions
# from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
        # if request.method == 'GET':       #HEAD and OPTION will also require a user to be admin
            return True
        return bool(request.user and request.user.is_staff)

class FullDjangoModelPermissions(permissions.DjangoObjectPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']