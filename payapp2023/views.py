from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Feature, UserProfile, Transaction, PaymentRequest
from .forms import CustomUserCreationForm, PaymentForm, PaymentRequestForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal  # Import Decimal for handling currency

def index(request):
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})

@login_required
def counter(request):
    words = request.POST.get('words', '')  # Use get method instead of accessing POST directly
    amount_of_word = len(words.split())
    return render(request, 'counter.html', {'amount': amount_of_word})

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

@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            try:
                recipient_profile = UserProfile.objects.get(user__username=recipient_username)
            except UserProfile.DoesNotExist:
                recipient_user = User.objects.get(username=recipient_username)
                recipient_profile = UserProfile.objects.create(user=recipient_user, balance=0)
            sender_profile = UserProfile.objects.get(user=request.user)
            sender_profile.balance -= amount
            sender_profile.save()
            recipient_profile.balance += amount
            recipient_profile.save()
            Transaction.objects.create(sender=request.user, recipient=recipient_profile.user, amount=amount)
            messages.success(request, 'Payment successfully sent.')
            return redirect('view_transactions')
    else:
        form = PaymentForm()
    return render(request, 'make_payment.html', {'form': form})

def user_logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(recipient=request.user)
    return render(request, 'view_transactions.html', {'transactions': transactions})

@login_required
def request_payment(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient_username']
            amount_requested = form.cleaned_data['amount']
            PaymentRequest.objects.create(
                sender=request.user,
                recipient=User.objects.get(username=recipient_username),
                amount=amount_requested
            )
            return redirect('success')
    else:
        form = PaymentRequestForm()
    return render(request, 'request_payments.html', {'form': form})

@login_required
def notification(request):
    pending_requests = PaymentRequest.objects.filter(recipient=request.user, status='pending')
    return render(request, 'notification.html', {'pending_requests': pending_requests})

@login_required
def handle_payment_request(request, request_id, action):
    payment_request = PaymentRequest.objects.get(id=request_id)
    if action == 'accept':
        # Update status to accepted
        payment_request.status = 'accepted'
        payment_request.save()
        return redirect('make_payment')  # Redirect to payment page
    elif action == 'reject':
        # Update status to rejected
        payment_request.status = 'rejected'
        payment_request.save()
        return redirect('index')  # Redirect to user's index page

@login_required
def view_accounts(request):
    users = User.objects.all()
    return render(request, 'view_accounts.html', {'users': users})

@staff_member_required
def view_user_accounts(request):
    users = User.objects.all()
    return render(request, 'user_accounts.html', {'users': users})

@staff_member_required
def view_all_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'all_transactions.html', {'transactions': transactions})

from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import UserProfile

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

def success(request):
    notification = request.session.get('payment_notification')
    if notification:
        recipient_username = notification.get('recipient_username')
        amount_requested = notification.get('amount_requested')
        return render(request, 'notification.html', {
            'recipient_username': recipient_username,
            'amount_requested': amount_requested,
        })
    else:
        return render(request, 'success.html')

def send_notification(request):
    requester_username = request.POST.get('requester_username')
    amount_requested = request.POST.get('amount_requested')
    recipient_user = User.objects.get(username='recipient_username')
    context = {

        'recipient_username': recipient_user.username,
        'amount_requested': amount_requested,
    }
    return render(request, 'notification.html', context)


