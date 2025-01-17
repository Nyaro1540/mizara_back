from django.db import models
from django.contrib.auth.models import AbstractUser ,Group, Permission

class Collecteur(AbstractUser):
    # Le Collecteur hérite des fonctionnalités de l'AbstractUser (gestion de l'authentification par défaut)
    CIN = models.CharField(max_length=20, unique=True)  # Numéro CIN unique
    phone_number = models.CharField(max_length=15, unique=True)  # Numéro de téléphone valide
    photo_cin = models.ImageField(upload_to='collecteurs/cin/', null=True, blank=True)  # Photo du CIN
    photo_nif = models.ImageField(upload_to='collecteurs/nif/', null=True, blank=True)  # Photo du NIF (si nécessaire)
    mobile_money_name = models.CharField(max_length=100)  # Nom inscrit sur Mobile Money
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Verified', 'Verified')], default='Pending')
    
    # Champ supplémentaire si besoin de stockage d'autres informations spécifiques
    address = models.TextField(null=True, blank=True)
    
    # Champs hérités d'AbstractUser avec un related_name unique pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        related_name='collecteur_set',  # Nom de la relation inverse
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='collecteur_permissions',  # Nom de la relation inverse
        blank=True
    )

    def __str__(self):
        return self.username  # Retourne le nom d'utilisateur (qui est une donnée de base dans AbstractUser)
    
    class Meta:
        verbose_name = "Collecteur"
        verbose_name_plural = "Collecteurs"

class Client(AbstractUser):
    # Le Client hérite aussi d'AbstractUser (pour la gestion par défaut de l'authentification)
    phone_number = models.CharField(max_length=15, unique=True)  # Numéro de téléphone valide
    mobile_money_name = models.CharField(max_length=100)  # Nom inscrit sur Mobile Money
    is_company = models.BooleanField(default=False)  # Indique si c'est un particulier ou une entreprise
    company_name = models.CharField(max_length=200, null=True, blank=True)  # Nom de l'entreprise si applicable
    company_nif = models.CharField(max_length=50, null=True, blank=True)  # NIF de l'entreprise si applicable
    company_contact_name = models.CharField(max_length=100, null=True, blank=True)  # Nom du responsable des achats
    company_phone_number = models.CharField(max_length=15, null=True, blank=True)  # Numéro de téléphone de l'entreprise

    # Ajout des relations many-to-many avec un related_name unique
    groups = models.ManyToManyField(
        Group,
        related_name='client_set',  # Nom de la relation inverse
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='client_permissions',  # Nom de la relation inverse
        blank=True
    )

    # Méthodes supplémentaires pour les champs ImageField si nécessaire
    # photo_cin = models.ImageField(upload_to='client_photos/cin/', blank=True, null=True)
    # photo_nif = models.ImageField(upload_to='client_photos/nif/', blank=True, null=True)

    def __str__(self):
        return self.username  # Retourne le nom d'utilisateur (également gestion de l'authentification)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Organisme(models.Model):
    # Informations de base sur l'organisme
    name = models.CharField(max_length=200)  # Nom de l'organisme
    address = models.TextField()  # Adresse physique de l'organisme
    description = models.TextField()  # Description de l'organisation
    contact_email = models.EmailField()  # Email de contact
    phone_number = models.CharField(max_length=15, unique=True)  # Numéro de téléphone de contact
    mobile_money_name = models.CharField(max_length=100)  # Nom inscrit sur Mobile Money
    #logo = models.ImageField(upload_to='organismes/logos/', null=True, blank=True)  # Logo de l'organisme (optionnel)
    
    # Méthodes utiles
    def __str__(self):
        return self.name  # Retourne le nom de l'organisme comme identifiant
    
    class Meta:
        verbose_name = "Organisme de Don"
        verbose_name_plural = "Organismes de Don"

class Don(models.Model):
    # Informations relatives au don
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Montant du don
    donor = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Utilisateur qui fait le don
    organisme = models.ForeignKey(Organisme, on_delete=models.CASCADE)  # Organisme destinataire du don
    donation_date = models.DateTimeField(auto_now_add=True)  # Date du don
    transaction_id = models.CharField(max_length=100, unique=True)  # Identifiant unique de la transaction (pour traçabilité)

    def __str__(self):
        return f"{self.donor.username} -> {self.organisme.name} : {self.amount} MGA"

    class Meta:
        verbose_name = "Don"
        verbose_name_plural = "Dons"
