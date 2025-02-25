from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionMvolaViewSet, TransactionAirtelMoneyViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionMvolaViewSet)
router.register(r'airtel-transactions', TransactionAirtelMoneyViewSet)

router = DefaultRouter()
router.register(r'transactions', TransactionMvolaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
