from django.db import models
from utilisateurs.models import User

class Offre(models.Model):
    TYPE_CHOICES = [
        ('legume', 'Légume'),
        ('fruit', 'Fruit'),
        ('viande', 'Viande'),
        ('poisson', 'Poisson'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archivee', 'Archivée'),
    ]

    producteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offres')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='offres/', blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')
    type_offre = models.CharField(max_length=20, choices=TYPE_CHOICES, default='legume')
    prix_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix en Ariary par kilogramme")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Offre'
        verbose_name_plural = 'Offres'

    def __str__(self):
        return self.titre
