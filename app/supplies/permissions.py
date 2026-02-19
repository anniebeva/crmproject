from rest_framework import permissions

class SupplyPermissions(permissions.BasePermission):
    """Allows access to supplies info and actions only to company owner and employees"""

    def has_object_permission(self, request, view, obj):
        user = request.user

        return obj.company == user.company