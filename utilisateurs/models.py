from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from datetime import timedelta
from random import randint
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('collecteur', 'Collecteur'),
        ('agent', 'Agent de réception'),
    ]
    nom_complet = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)  # Ajout du champ prenom
    numero_telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    lieu_habitation = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    numero_telephone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    verification_code = models.IntegerField(null=True, blank=True)
    verification_code_expiry = models.DateTimeField(null=True, blank=True)
    verification_attempts = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'numero_telephone'
    REQUIRED_FIELDS = ['nom_complet', 'email']

    objects = UserManager()

    def __str__(self):
        return self.nom_complet
    
    # Redéfinir les champs groups et user_permissions avec related_name uniques
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to...',
        related_name="utilisateurs_user_groups",  # Nom unique
        related_query_name="utilisateur_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user...',
        related_name="utilisateurs_user_permissions",  # Nom unique
        related_query_name="utilisateur_user_permission",
    )

    def set_verification_code(self):
        self.verification_code = randint(100000, 999999)
        self.verification_code_expiry = timezone.now() + timedelta(minutes=10)
        self.verification_attempts = 0
        self.save()


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def blacklist(cls, token):
        """Ajoute un token à la liste noire"""
        cls.objects.create(token=str(token))

    @classmethod
    def is_blacklisted(cls, token):
        """Vérifie si un token est dans la liste noire"""
        return cls.objects.filter(token=str(token)).exists()

class Utilisateurs(models.Model):
    # Your Utilisateurs model fields here
    pass