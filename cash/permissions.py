from rest_framework.permissions import BasePermission
from accounts.models import Profile

"""class IsAdminUserRole(BasePermission):

    message = 'Bu sayfaya yalnızca admin kullanıcılar erişebilir.'
    def has_permission(self, request, view):
        try:
            return request.user.is_authenticated and request.user.profile.role == 'AD'
        except Profile.DoesNotExist:
            return False
"""
class IsAdminUserRole(BasePermission):
    message = 'Bu sayfaya yalnızca admin kullanıcılar erişebilir.'
    """def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == 'AD'"""

    def has_permission(self, request, view):
        print("Permission check, user:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        print("Is staff:", request.user.is_staff)
        print("Is superuser:", request.user.is_superuser)
        return bool(request.user and request.user.is_staff)
