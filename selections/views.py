from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from selections.permissions import IsUsersSelection
from selections.serializers import *


# ----------------------------------------------------------------
# Paginator
class Paginator(PageNumberPagination):
    """
    Custom pagination class
    """
    page_size: int = 4


# ----------------------------------------------------------------
# SelectionViewSet
class SelectionViewSet(ModelViewSet):
    queryset: QuerySet = Selection.objects.all()
    default_serializer: SelectionUpdateSerializer = SelectionUpdateSerializer
    serializers: dict = {
        'list': SelectionListSerializer,
        'retrieve': SelectionDetailSerializer,
        'create': SelectionCreateSerializer,
        'destroy': SelectionDeleteSerializer
    }
    permissions: dict = {
        'create': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsUsersSelection()],
        'partial_update': [IsAuthenticated(), IsUsersSelection()],
        'destroy': [IsAuthenticated(), IsUsersSelection()]
    }
    pagination_class: Paginator = Paginator

    def get_serializer_class(self):
        """
        Method to define serializer class
        """
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self) -> list:
        """
        Method to define permissions
        :return: list with permission
        """
        if self.action == 'create':
            return self.permissions.get('create')
        if self.action == 'update':
            return self.permissions.get('update')
        if self.action == 'partial_update':
            return self.permissions.get('partial_update')
        if self.action == 'destroy':
            return self.permissions.get('destroy')
        return []
