from rest_framework import serializers
from .models import Commande
from utilisateurs.serializers import UserSerializer
from marketplace.serializers import OffreSerializer

class CommandeSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    offre = OffreSerializer(read_only=True)
    
    class Meta:
        model = Commande
        fields = ['id', 'client', 'offre', 'quantite', 'date_commande', 'statut', 'commentaire']
        read_only_fields = ['id', 'date_commande', 'client']

class CreateCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = ['offre', 'quantite', 'commentaire']
