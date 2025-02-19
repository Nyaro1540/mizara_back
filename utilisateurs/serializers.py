from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, ProfileCollecteur

class ProfileCollecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCollecteur
        fields = ['nif', 'stat', 'cin']

class UserSerializer(serializers.ModelSerializer):
    profile_collecteur = ProfileCollecteurSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'nom_complet', 'prenom', 'numero_telephone', 'email', 'lieu_habitation', 'role', 'profile_collecteur']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['nom_complet', 'prenom', 'numero_telephone', 'email', 'lieu_habitation', 'password', 'password_confirmation']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')  # On enlève le champ password_confirmation
        user = User.objects.create_user(**validated_data)
        return user
