from django.db import models

class TransactionAirtelMoney(models.Model):
    user = models.ForeignKey('utilisateurs.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)  # e.g., 'pending', 'completed', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.transaction_id} - {self.amount} Ariary'

from django.db import models

class TransactionMvola(models.Model):
    user = models.ForeignKey('utilisateurs.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)  # e.g., 'pending', 'completed', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.transaction_id} - {self.amount} Ariary'
