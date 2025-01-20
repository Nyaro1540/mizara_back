from rest_framework.routers import DefaultRouter
from .views import CollecteurViewSet, ClientViewSet, OrganismeViewSet, DonViewSet

router = DefaultRouter()
router.register(r'collecteurs', CollecteurViewSet, basename='collecteur')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'organismes', OrganismeViewSet, basename='organisme')
router.register(r'dons', DonViewSet, basename='don')

urlpatterns = router.urls
