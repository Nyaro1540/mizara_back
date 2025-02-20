from django.contrib import admin
from .models import Commande

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'offre', 'quantite', 'statut', 'date_commande')
    list_filter = ('statut', 'date_commande')
    search_fields = ('client__email', 'offre__titre')
    ordering = ('-date_commande',)
