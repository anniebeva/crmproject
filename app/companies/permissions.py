from rest_framework.permissions import BasePermission, SAFE_METHODS

class CompanyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_company_owner:
            pass
