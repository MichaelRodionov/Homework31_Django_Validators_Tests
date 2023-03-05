from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from locations.models import Location
from locations.serializers import LocationSerializer


# ----------------------------------------------------------------
# Paginator
class Paginator(PageNumberPagination):
    """
    Custom pagination class
    """
    page_size: int = 4


# ----------------------------------------------------------------
# Location ViewSet
class LocationViewSet(ModelViewSet):
    queryset: QuerySet = Location.objects.all()
    serializer_class: LocationSerializer = LocationSerializer
    pagination_class: Paginator = Paginator
