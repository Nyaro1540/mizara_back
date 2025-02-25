from rest_framework import serializers
from .models import TransactionMvola, TransactionAirtelMoney

class TransactionAirtelMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionAirtelMoney
        fields = ['id', 'user', 'amount', 'transaction_id', 'status', 'created_at']

class TransactionMvolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionMvola
        fields = ['id', 'user', 'amount', 'transaction_id', 'status', 'created_at']
