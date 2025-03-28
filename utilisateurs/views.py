from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, ProfileCollecteur
from .serializers import UserSerializer, RegisterSerializer, ProfileCollecteurSerializer
from django.core.mail import send_mail
from random import randint
from django.utils import timezone

# 1. Inscription (Register)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# 2. Connexion (Login)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")  # Peut être email ou numéro de téléphone
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"error": "Email/Numéro de téléphone et mot de passe requis."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        user = None
        try:
            if '@' in identifier:  # Si c'est un email
                user = User.objects.filter(email=identifier).first()
            else:  # Si c'est un numéro de téléphone
                user = User.objects.filter(numero_telephone=identifier).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "nom_complet": user.nom_complet,
                        "role": user.role
                    }
                }
                # Ajouter une URL de redirection pour les administrateurs
                if user.role == 'admin':
                    response_data["redirect_url"] = "/admin/dashboard/"
                return Response(response_data, status=status.HTTP_200_OK)
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "Une erreur s'est produite lors de l'authentification."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 3. Déconnexion (Logout)
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

# 4. Réinitialisation de mot de passe - Demande
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        numero_telephone = request.data.get("phone_number")
        email = request.data.get("email")

        if not numero_telephone and not email:
            return Response({"error": "Numéro de téléphone ou adresse e-mail requis."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = None
        if numero_telephone:
            user = User.objects.filter(numero_telephone=numero_telephone).first()
        elif email:
            user = User.objects.filter(email=email).first()
            if user and user.email != email:
                return Response({"error": "L'adresse email ne correspond pas à celle enregistrée."}, 
                              status=status.HTTP_400_BAD_REQUEST)

        if user is None:
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Générer et enregistrer un code de vérification
        user.set_verification_code()

        # Envoyer le code par SMS ou e-mail
        try:
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
            
            # Limiter les tentatives de réinitialisation
            if user.verification_attempts >= 5:
                return Response({"error": "Nombre maximum de tentatives atteint. Veuillez réessayer plus tard."}, 
                              status=status.HTTP_429_TOO_MANY_REQUESTS)

            return Response({
                "message": "Code de vérification envoyé.",
                "expires_in": 600  # 10 minutes en secondes
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Erreur lors de l'envoi du code de vérification : {str(e)}")
            return Response({
                "error": "Une erreur s'est produite lors de l'envoi du code de vérification",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 5. Réinitialisation de mot de passe - Confirmation
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        numero_telephone = request.data.get("numero_telephone")
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")
        new_password = request.data.get("new_password")

        if not verification_code or not new_password:
            return Response({"error": "Code de vérification et nouveau mot de passe requis."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = None
        if numero_telephone:
            user = User.objects.filter(numero_telephone=numero_telephone, verification_code=verification_code).first()
        elif email:
            user = User.objects.filter(email=email, verification_code=verification_code).first()

        if user is None:
            if user:
                user.verification_attempts += 1
                user.save()
            return Response({"error": "Code de vérification invalide ou utilisateur non trouvé."}, 
                          status=status.HTTP_404_NOT_FOUND)

        if user.verification_code_expiry < timezone.now():
            user.verification_attempts += 1
            user.save()
            return Response({"error": "Code de vérification expiré."}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_attempts >= 5:
            return Response({
                "error": "Nombre de tentatives dépassé.",
                "remaining_time": int((user.verification_code_expiry - timezone.now()).total_seconds())
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            user.set_password(new_password)
            user.verification_code = None
            user.verification_code_expiry = None
            user.verification_attempts = 0
            user.save()

            return Response({
                "message": "Mot de passe réinitialisé avec succès.",
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Erreur lors de la réinitialisation du mot de passe : {str(e)}")
            return Response({
                "error": "Une erreur s'est produite lors de la réinitialisation du mot de passe",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 6. Profil Collecteur
class ProfileCollecteurView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = ProfileCollecteur.objects.get(user=request.user)
            # Vérifier la cohérence du rôle
            if request.user.role != 'collecteur':
                request.user.role = 'collecteur'
                request.user.save()
            serializer = ProfileCollecteurSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProfileCollecteur.DoesNotExist:
            return Response({"error": "Profil collecteur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Vérifier si l'utilisateur a déjà un profil collecteur
        if ProfileCollecteur.objects.filter(user=request.user).exists():
            return Response({"error": "Un profil collecteur existe déjà pour cet utilisateur"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        nif = request.data.get("nif")
        stat = request.data.get("stat")
        cin = request.data.get("cin")

        if not nif or not stat or not cin:
            return Response({"error": "NIF, STAT et CIN sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = ProfileCollecteurSerializer(data=data)
        
        if serializer.is_valid():
            # Sauvegarder le profil collecteur
            serializer.save()
            # Mettre à jour le rôle de l'utilisateur en 'collecteur' (remplace complètement le rôle précédent)
            request.user.role = 'collecteur'
            request.user.save()
            
            return Response({
                "message": "Profil collecteur créé avec succès. Votre rôle a été définitivement mis à jour en 'collecteur'.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # Vérifier si l'utilisateur a un profil collecteur
        try:
            profile = ProfileCollecteur.objects.get(user=request.user)
        except ProfileCollecteur.DoesNotExist:
            return Response({"error": "Profil collecteur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        # Mettre à jour le rôle si ce n'est pas déjà fait
        if request.user.role != 'collecteur':
            request.user.role = 'collecteur'
            request.user.save()

        serializer = ProfileCollecteurSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 7. Complétion du profil collecteur
class CompleteProfileCollecteurView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # Vérifier si l'utilisateur a un profil collecteur
        if not ProfileCollecteur.objects.filter(user=user).exists():
            return Response({"error": "Vous devez d'abord créer un profil collecteur"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le rôle définitivement
        user.role = 'collecteur'
        user.save()

        return Response({
            "message": "Votre profil collecteur est complet. Votre rôle a été définitivement mis à jour en 'collecteur'."
        }, status=status.HTTP_200_OK)

# 8. Upload photo de profil
@api_view(['POST'])
def upload_profile_picture(request):
    user = request.user
    if request.method == 'POST':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)