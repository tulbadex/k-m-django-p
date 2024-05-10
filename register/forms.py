from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class CustomUserCreationForm(UserCreationForm):
    CURRENCY_CHOICES = [
        ('GBP', 'GB Pounds'),
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
    ]
    username = forms.CharField(max_length=150, required=True, help_text='Required. Unique.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.CharField(max_length=150, required=True, validators=[EmailValidator], help_text='Must be a valid email address.')
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Your password must contain at least 8 characters.",
        required=True
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
        required=True,
    )
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User  # Use the built-in User model
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency')

