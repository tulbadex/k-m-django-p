from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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
    details = models.TextField(max_length=500)

from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp to the current time when the transaction is created

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.amount}"

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for administrator profile

from django.contrib.auth.models import AbstractUser

# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    CURRENCY_CHOICES = [
        ('GBP', 'GB Pounds'),
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
    ]
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User  # Use the built-in User model
        fields = ('username', 'email', 'password1', 'password2', 'currency')

from django.db import models
from django.contrib.auth.models import User

# models.py


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Set a default value

    # Other fields and methods of UserProfile

    CURRENCY_CHOICES = [
        ('GBP', 'GB Pounds'),
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')

    def __str__(self):
        return self.user.username



