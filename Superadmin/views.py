from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utilisateurs.models import User
from .models import Publication, Transaction
from .serializers import PublicationSerializer, TransactionSerializer

# User Management View
class UserManagementView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# Publication Management View
class PublicationManagementView(generics.ListCreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        publications = self.get_queryset()
        serializer = self.get_serializer(publications, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        publication = serializer.save()
        return Response({"message": "Publication created successfully"}, status=status.HTTP_201_CREATED)

# Transaction Management View
class TransactionManagementView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        transactions = self.get_queryset()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
