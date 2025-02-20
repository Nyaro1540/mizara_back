from django.contrib import admin
from .models import Offre

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'producteur', 'titre', 'type_offre', 'prix_kg', 'statut', 'date_creation')
    list_filter = ('type_offre', 'statut', 'date_creation')
    search_fields = ('titre', 'producteur__email')
    ordering = ('-date_creation',)
