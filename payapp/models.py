from django.db import models
from django.contrib.auth.models import User

class PaymentRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_payment_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_payment_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # Status: pending, accepted, rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment request from {self.sender.username} to {self.recipient.username}"


class Feature(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=400)

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp to the current time when the transaction is created

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.amount}"