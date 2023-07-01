from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class JobPostPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return True

        return user.is_authenticated and (user.is_acs or user.is_external)
