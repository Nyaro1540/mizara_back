from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import TransactionMvola, TransactionAirtelMoney
from .serializers import TransactionMvolaSerializer, TransactionAirtelMoneySerializer

class TransactionAirtelMoneyViewSet(viewsets.ModelViewSet):
    queryset = TransactionAirtelMoney.objects.all()
    serializer_class = TransactionAirtelMoneySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionMvolaViewSet(viewsets.ModelViewSet):
    queryset = TransactionMvola.objects.all()
    serializer_class = TransactionMvolaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
