from django.contrib import admin
from .models import Collecteur, Client, Organisme, Don

@admin.register(Collecteur)
class CollecteurAdmin(admin.ModelAdmin):
    list_display = ('username', 'CIN', 'phone_number', 'status')
    search_fields = ('username', 'CIN', 'phone_number')
    list_filter = ('status',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_company')
    search_fields = ('username', 'phone_number', 'company_name')

@admin.register(Organisme)
class OrganismeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'contact_email')
    search_fields = ('name', 'phone_number')

@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display = ('donor', 'organisme', 'amount', 'donation_date')
    search_fields = ('donor__username', 'organisme__name', 'transaction_id')
    list_filter = ('donation_date',)
