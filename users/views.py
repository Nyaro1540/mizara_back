from rest_framework import viewsets, permissions
from .models import Collecteur, Client, Organisme, Don
from .serializers import CollecteurSerializer, ClientSerializer, OrganismeSerializer, DonSerializer

# Collecteur ViewSet
class CollecteurViewSet(viewsets.ModelViewSet):
    queryset = Collecteur.objects.all()
    serializer_class = CollecteurSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restriction aux utilisateurs authentifiés
    filterset_fields = ['status', 'CIN']  # Permet de filtrer sur le statut et le CIN
    search_fields = ['username', 'phone_number']  # Recherche par nom d'utilisateur et téléphone

# Client ViewSet
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_company']  # Filtrer les clients par entreprise ou particulier
    search_fields = ['username', 'phone_number', 'company_name']

# Organisme ViewSet
class OrganismeViewSet(viewsets.ModelViewSet):
    queryset = Organisme.objects.all()
    serializer_class = OrganismeSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'phone_number', 'contact_email']

# Don ViewSet
class DonViewSet(viewsets.ModelViewSet):
    queryset = Don.objects.all()
    serializer_class = DonSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['donation_date', 'organisme', 'donor']  # Filtrer les dons par date, organisme, ou donateur
    search_fields = ['transaction_id', 'organisme__name', 'donor__username']
