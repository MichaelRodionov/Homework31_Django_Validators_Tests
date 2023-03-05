from rest_framework import permissions

from authentication.models import User


# ----------------------------------------------------------------
# This class defines user's permissions or user's role to edit advertisement
class IsUsersAdOrUserAdmin(permissions.BasePermission):
    message: str = 'You are not allowed to edit or delete this advertisement'

    def has_object_permission(self, request, view, obj) -> bool:
        return str(obj.author.id) == str(request.user.id) or request.user.role == User.Roles.ADMIN
