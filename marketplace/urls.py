from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OffreViewSet

router = DefaultRouter()
router.register(r'offres', OffreViewSet, basename='offre')

urlpatterns = [
    path('', include(router.urls)),
]
