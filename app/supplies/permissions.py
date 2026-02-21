from rest_framework import permissions

class SupplyPermissions(permissions.BasePermission):
    """Allows access to supplies info and actions only to company owner and employees"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'company')

    def has_object_permission(self, request, view, obj):
        user = request.user

        return obj.supplier.company == user.company