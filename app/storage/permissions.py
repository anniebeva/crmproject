from rest_framework import permissions


class StoragePermission(permissions.BasePermission):
    """
    Allows viewing access to all employees, edit/delete/create only to company-owner
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.is_company_owner
        return True

    def has_object_permission(self, request, view, obj):

        user = request.user

        if obj.company != user.company:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_company_owner