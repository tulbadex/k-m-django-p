from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal  # Import Decimal for handling currency
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import UserProfile
from payapp.models import Feature

def index(request):
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def user_logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Convert currency to appropriate initial amount
            currency = form.cleaned_data['currency']
            if currency == 'GBP':
                initial_balance = Decimal(1000)  # Initial amount for GBP
            elif currency == 'USD':
                initial_balance = Decimal(1000) * Decimal(1.35)  # Initial amount for USD (assuming 1 GBP = 1.35 USD)
            elif currency == 'EUR':
                initial_balance = Decimal(1000) * Decimal(1.18)  # Initial amount for EUR (assuming 1 GBP = 1.18 EUR)
            else:
                initial_balance = Decimal(1000)  # Default to GBP
            
            # Create UserProfile with initial balance
            UserProfile.objects.create(user=user, currency=currency, balance=initial_balance)
            
            # Log in the user
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



