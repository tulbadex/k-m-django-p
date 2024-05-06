from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    CURRENCY_CHOICES = [
        ('GBP', 'GB Pounds'),
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
    ]
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User  # Use the built-in User model
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency')

