from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for administrator profile


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



