from rest_framework import viewsets, permissions
from .models import Commande
from .serializers import CommandeSerializer, CreateCommandeSerializer
from rest_framework.response import Response
from rest_framework import status

class CommandeViewSet(viewsets.ModelViewSet):
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Commande.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCommandeSerializer
        return CommandeSerializer

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
