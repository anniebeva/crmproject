from rest_framework import permissions

class SupplyPermissions(permissions.BasePermission):
    """Allows access to supplies' info and actions only to company owner and employees"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.company

    def has_object_permission(self, request, view, obj):
        return obj.supplier.company == request.user.company