from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import utilisateurs
from .serializers import UserSerializer, RegisterSerializer
from django.core.mail import send_mail
from random import randint
from django.utils import timezone

# 📌 1. Inscription (Register)
class RegisterView(generics.CreateAPIView):
    queryset = utilisateurs.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# 📌 2. Connexion (Login)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        numero_telephone = request.data.get("phone_number")
        password = request.data.get("password")

        if not numero_telephone or not password:
            return Response({"error": "Numéro de téléphone et mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(numero_telephone=numero_telephone, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

# 📌 3. Déconnexion (Logout)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        numero_telephone = request.data.get("phone_number")
        email = request.data.get("email")

        if not numero_telephone and not email:
            return Response({"error": "Numéro de téléphone ou adresse e-mail requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        if numero_telephone:
            user = utilisateurs.objects.filter(numero_telephone=numero_telephone).first()
        elif email:
            user = utilisateurs.objects.filter(email=email).first()

        if user is None:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Générer et enregistrer un code de vérification
        user.set_verification_code()

        # Envoyer le code par SMS ou e-mail
        if numero_telephone:
            # Envoyer le code par SMS (implémentation dépendante de votre fournisseur de SMS)
            pass
        elif email:
            send_mail(
                'Réinitialisation de mot de passe',
                f'Votre code de vérification est {user.verification_code}',
                'noreply@votresite.com',
                [email],
                fail_silently=False,
            )

        return Response({"message": "Code de vérification envoyé."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        numero_telephone = request.data.get("numero_telephone")
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")
        new_password = request.data.get("new_password")

        if not verification_code or not new_password:
            return Response({"error": "Code de vérification et nouveau mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        if numero_telephone:
            user = utilisateurs.objects.filter(numero_telephone=numero_telephone, verification_code=verification_code).first()
        elif email:
            user = utilisateurs.objects.filter(email=email, verification_code=verification_code).first()

        if user is None:
            return Response({"error": "Code de vérification invalide ou utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        if user.verification_code_expiry < timezone.now():
            return Response({"error": "Code de vérification expiré."}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_attempts >= 5:
            return Response({"error": "Nombre de tentatives dépassé."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.verification_code = None
        user.verification_code_expiry = None
        user.verification_attempts = 0
        user.save()

        return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
