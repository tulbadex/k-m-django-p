from django import forms
from django.contrib.auth.models import User





class PaymentRequestForm(forms.Form):
    recipient_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_recipient_username(self):
        recipient_username = self.cleaned_data['recipient_username']
        try:
            User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            raise forms.ValidationError("Recipient does not exist.")
        return recipient_username


class PaymentForm(forms.Form):
    recipient_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


    def clean_recipient_username(self):
        recipient_username = self.cleaned_data['recipient_username']
        try:
            User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            raise forms.ValidationError('Recipient username does not exist.')
        return recipient_username

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

