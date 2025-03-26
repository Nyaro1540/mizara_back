from django.urls import path
from .views import UserManagementView, PublicationManagementView, TransactionManagementView, ProfileCollecteurCreateView

urlpatterns = [
    path('users/', UserManagementView.as_view(), name='user-management'),
    path('publications/', PublicationManagementView.as_view(), name='publication-management'),
    path('transactions/', TransactionManagementView.as_view(), name='transaction-management'),
    path('collecteur/profile/', ProfileCollecteurCreateView.as_view(), name='collecteur-profile-create'),  # New endpoint for collector profile
]
