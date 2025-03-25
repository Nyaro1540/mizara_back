from django.contrib import admin
from .models import Publication, Transaction, Report

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')
    search_fields = ('title',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_date', 'status')
    search_fields = ('user__nom_complet',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
