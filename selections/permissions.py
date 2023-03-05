from rest_framework import permissions


# ----------------------------------------------------------------
# This class defines user's permissions to edit or delete selection
class IsUsersSelection(permissions.BasePermission):
    message: str = 'You are not allowed to edit or delete this selection'

    def has_object_permission(self, request, view, obj) -> bool:
        """Method to check user's access"""
        if str(obj.owner.id) == str(request.user.id):
            return True
        return False
