from django.db.models import QuerySet
from django.http import JsonResponse
from requests import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.permissions import IsUsersAdOrUserAdmin
from ads.serializers import *


# ----------------------------------------------------------------
# FBV
def check_response(request) -> JsonResponse:
    """
    start page function to give status OK response
    :param request: request
    :return: JsonResponse
    """
    return JsonResponse({
        'status': 'OK'
    }, status=200)


# ----------------------------------------------------------------
# Paginator
class Paginator(PageNumberPagination):
    """
    Custom pagination class
    """
    page_size: int = 10


# ----------------------------------------------------------------
# CategoryViewSet
class CategoryViewSet(ModelViewSet):
    """
    PUT, PATCH, DELETE requests set CatChangeSerializer as a default serializer,
    other requests - one of serializers: dict
    """
    queryset: QuerySet = Category.objects.all()
    default_serializer: CatChangeSerializer = CatChangeSerializer
    serializers: dict = {
        'list': CatListDetailSerializer,
        'retrieve': CatListDetailSerializer,
        'create': CatCreateSerializer,
    }

    def get_serializer_class(self) -> CatChangeSerializer:
        """
        Method to define serializer class
        :return: CatChangeSerializer
        """
        return self.serializers.get(self.action, self.default_serializer)


# ----------------------------------------------------------------
# Advertisement ViewSet
class AdvertisementViewSet(ModelViewSet):
    """
    PUT, PATCH, DELETE requests set AdChangeSerializer as a default serializer,
    other requests - one of serializers: dict
    """
    queryset: QuerySet = Advertisement.objects.all()
    default_serializer: AdChangeSerializer = AdChangeSerializer
    serializers: dict = {
        'list': AdListDetailSerializer,
        'retrieve': AdListDetailSerializer,
        'create': AdCreateSerializer,
    }
    pagination_class: Paginator = Paginator
    permissions: dict = {
        'retrieve': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsUsersAdOrUserAdmin()],
        'partial_update': [IsAuthenticated(), IsUsersAdOrUserAdmin()],
        'destroy': [IsAuthenticated(), IsUsersAdOrUserAdmin()]
    }

    def get_permissions(self) -> list:
        """
        Method to define permissions
        :return: list with permission
        """
        if self.action == 'retrieve':
            return self.permissions.get('retrieve')
        if self.action == 'update':
            return self.permissions.get('update')
        if self.action == 'partial_update':
            return self.permissions.get('partial_update')
        if self.action == 'destroy':
            return self.permissions.get('destroy')
        return []

    def get_serializer_class(self) -> AdChangeSerializer:
        """
        Method to define serializer class
        :return: AdChangeSerializer
        """
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs) -> Response:
        """
        Method to filter queryset by query parameters
        :param request: request
        :param args: positional arguments
        :param kwargs: keyword arguments
        :return: Response
        """
        cats: Any = request.GET.getlist('cat')
        text: Any = request.GET.get('text')
        location: Any = request.GET.get('location')
        price_from: Any = request.GET.get('price_from')
        price_to: Any = request.GET.get('price_to')

        if cats:
            self.queryset: QuerySet = self.queryset.filter(category_id__in=cats)
        if text:
            self.queryset: QuerySet = self.queryset.filter(name__icontains=text)
        if location:
            self.queryset: QuerySet = self.queryset.filter(author__locations__name__icontains=location)
        if price_from:
            self.queryset: QuerySet = self.queryset.filter(price__gt=price_from)
        if price_to:
            self.queryset: QuerySet = self.queryset.filter(price__lt=price_to)

        return super().list(self, request, *args, **kwargs)
