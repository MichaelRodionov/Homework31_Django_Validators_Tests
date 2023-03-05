from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from Homework31_Django_Validators_Tests import settings
from ads.views import *
from locations.views import LocationViewSet
from selections.views import *

# ----------------------------------------------------------------
# create SimpleRouter instance
router = SimpleRouter()


# ----------------------------------------------------------------
# register routers
router.register('ad', AdvertisementViewSet)
router.register('cat', CategoryViewSet)
router.register('location', LocationViewSet)
router.register('selection', SelectionViewSet)


# ----------------------------------------------------------------
# urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authentication.urls')),
]

urlpatterns += router.urls


# ----------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
