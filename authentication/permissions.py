from rest_framework import permissions

from authentication.models import User


# ----------------------------------------------------------------
# This class defines user's permissions or user's role to edit advertisement
class IsUserAdmin(permissions.BasePermission):
    message: str = 'You are not allowed to edit or delete this advertisement'

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.role == User.Roles.ADMIN
