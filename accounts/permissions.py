from rest_framework import permissions

class IsBusinessOrAdmin(permissions.BasePermission):
    """
    Faqat Business yoki Admin roliga ega foydalanuvchilar ruxsat oladi.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['business', 'admin'])
