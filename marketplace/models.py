from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class Offre(models.Model):
    CHOIX_STATUT = [
        ('active', 'Active'),
        ('sold_out', 'Épuisée'),
        ('cancelled', 'Annulée'),
    ]
    
    CHOIX_TYPE = [
        ('vente', 'Vente'),
        ('don', 'Don'),
    ]
    
    collecteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offres")
    type_offre = models.CharField(max_length=20, choices=CHOIX_TYPE, default='vente')
    titre = models.CharField(max_length=255)
    description = models.TextField()
    prix_par_kg = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_kg = models.PositiveIntegerField()
    localisation = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=CHOIX_STATUT, default='active')
    image = models.ImageField(upload_to='offres_images/', null=True, blank=True)
    cree_a = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.get_type_offre_display()}) - {self.collecteur.full_name}"
