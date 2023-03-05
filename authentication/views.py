from django.db.models import QuerySet, Q, Count
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsUserAdmin
from authentication.serializers import *


# ----------------------------------------------------------------
# Paginator
class Paginator(PageNumberPagination):
    """
    Custom pagination class
    """
    page_size: int = 4


# ----------------------------------------------------------------
# User views
class UserListView(ListAPIView):
    queryset: QuerySet = User.objects.annotate(total_ads=Count(
        'advertisement',
        filter=Q(advertisement__is_published=True))). \
        order_by('username')
    serializer_class: UserListDetailSerializer = UserListDetailSerializer
    permission_classes: tuple = (IsAuthenticated, IsUserAdmin,)
    pagination_class: Paginator = Paginator


class UserDetailView(RetrieveAPIView):
    queryset: QuerySet = User.objects.annotate(total_ads=Count(
        'advertisement',
        filter=Q(advertisement__is_published=True))). \
        order_by('username')
    serializer_class: UserListDetailSerializer = UserListDetailSerializer
    permission_classes: tuple = (IsAuthenticated, IsUserAdmin,)


class UserCreateView(CreateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class: UserCreateSerializer = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class: UserChangeSerializer = UserChangeSerializer
    permission_classes: tuple = (IsAuthenticated, IsUserAdmin,)


class UserDeleteView(DestroyAPIView):
    queryset: QuerySet = User.objects.all()
    serializer_class: UserDeleteSerializer = UserDeleteSerializer
    permission_classes: tuple = (IsAuthenticated, IsUserAdmin,)
