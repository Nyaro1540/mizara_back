from rest_framework import serializers
from .models import Collecteur, Client, Organisme, Don

class CollecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collecteur
        fields = ['id', 'username', 'CIN', 'phone_number', 'status']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'phone_number', 'is_company', 'company_name']

class OrganismeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisme
        fields = ['id', 'name', 'phone_number', 'contact_email']

class DonSerializer(serializers.ModelSerializer):
    donor = CollecteurSerializer(read_only=True)
    organisme = OrganismeSerializer(read_only=True)

    class Meta:
        model = Don
        fields = ['id', 'donor', 'organisme', 'amount', 'donation_date', 'transaction_id']
