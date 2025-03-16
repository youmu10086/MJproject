# myapp/permissions.py
from rest_framework import permissions
from account.models import CustomUser

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            user = request.user
            if isinstance(user, CustomUser) and user.role == 'customer':
                return True
        return False

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            user = request.user
            if isinstance(user, CustomUser) and user.role == 'admin':
                return True
        return False

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            user = request.user
            if isinstance(user, CustomUser) and user.role == 'manager':
                return True
        return False