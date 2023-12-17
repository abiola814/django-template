from rest_framework.permissions import BasePermission

from account.models import User


class IsRiskAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_detail = User.objects.get(user=request.user)
        except User.DoesNotExist:
            return False
        if user_detail.role == "risk":
            return True
        else:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_detail = User.objects.get(user=request.user)
        except User.DoesNotExist:
            return False
        if user_detail.role == "admin":
            return True
        else:
            return False


class IsPrivilegedAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_detail = User.objects.get(user=request.user)
        except User.DoesNotExist:
            return False
        if user_detail.role == "privileged":
            return True
        else:
            return False


class IsHelpDeskAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_detail = User.objects.get(user=request.user)
        except User.DoesNotExist:
            return False
        if user_detail.role == "helpdesk":
            return True
        else:
            return False


