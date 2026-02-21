from rest_framework import permissions

class SupplierPermission(permissions.BasePermission):
    """Allows access to suppliers info and actions only to company owner and employees"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated or not hasattr(request.user, 'company'):
            return False

        if request.method == 'POST':
            company_id = request.data.get('company')
            if not company_id:
                return False
            return str(request.user.company.id) == str(company_id)

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.company == user.company
