from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Offre
from .serializers import OffreSerializer
from utilisateurs.models import User

class OffreViewSet(viewsets.ModelViewSet):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(collecteur=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        statut = self.request.query_params.get('statut', None)
        type_offre = self.request.query_params.get('type_offre', None)
        collecteur = self.request.query_params.get('collecteur', None)

        if statut:
            queryset = queryset.filter(statut=statut)
        if type_offre:
            queryset = queryset.filter(type_offre=type_offre)
        if collecteur:
            queryset = queryset.filter(collecteur__id=collecteur)

        return queryset.order_by('-cree_a')
