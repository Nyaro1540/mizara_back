from django.contrib import admin
from .models import Offre

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_offre', 'collecteur', 'statut', 'cree_a')
    list_filter = ('type_offre', 'statut')
    search_fields = ('titre', 'description', 'collecteur__username')
    ordering = ('-cree_a',)
