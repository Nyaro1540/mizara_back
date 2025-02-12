from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import utilisateurs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = utilisateurs
        fields = ['id', 'nom_complet', 'prenom', 'numero_telephone', 'email', 'lieu_habitation', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = utilisateurs
        fields = ['nom_complet', 'prenom', 'numero_telephone', 'email', 'lieu_habitation', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # On enlève le champ password2
        user = utilisateurs.objects.create_user(**validated_data)
        return user
