from django.db import models
from utilisateurs.models import User
from marketplace.models import Offre

class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('livree', 'Livrée'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='commandes')
    quantite = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_commande']
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return f'Commande #{self.id} - {self.offre.titre}'
