from rest_framework import permissions


class CompanyPermission(permissions.BasePermission):
    """
    Allow access only to company-owner
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_company_owner and request.user.company == obj
