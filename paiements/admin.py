from django.contrib import admin
from .models import TransactionMvola, TransactionAirtelMoney

@admin.register(TransactionAirtelMoney)
class TransactionAirtelMoneyAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__email')

@admin.register(TransactionMvola)
class TransactionMvolaAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__email')
