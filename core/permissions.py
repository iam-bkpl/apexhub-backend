from rest_framework.decorators import permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class AcsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_acs
