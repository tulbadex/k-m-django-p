from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Feature, Transaction, PaymentRequest
from .forms import PaymentForm, PaymentRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from register.models import UserProfile

from django.http import JsonResponse
from django.http import HttpResponseBadRequest

def index(request):
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})

@login_required
def counter(request):
    words = request.POST.get('words', '')  # Use get method instead of accessing POST directly
    amount_of_word = len(words.split())
    return render(request, 'counter.html', {'amount': amount_of_word})

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


ALLOWED_CURRENCIES = ['USD', 'EUR', 'GBP']  # Example list of allowed currencies
CONVERSION_RATES = {
    ('USD', 'EUR'): 0.93,  # Conversion rate from USD to EUR
    ('EUR', 'USD'): 1.08,  # Conversion rate from EUR to USD
    ('USD', 'GBP'): 0.80,  # Conversion rate from USD to GBP
    ('GBP', 'USD'): 1.26,  # Conversion rate from GBP to USD
    # Add more conversion rates as needed
}

def convert_currency(request, currency1, currency2, amount):

    try:
        amount = float(amount)
    except ValueError:
        return HttpResponseBadRequest('Amount must be a valid floating point number.')
    
    if currency1 not in ALLOWED_CURRENCIES or currency2 not in ALLOWED_CURRENCIES:
        return HttpResponseBadRequest('One or both of the provided currencies are not supported.')

    if (currency1, currency2) not in CONVERSION_RATES:
        return HttpResponseBadRequest('Conversion rate not available for the provided currency pair.')

    conversion_rate = CONVERSION_RATES[(currency1, currency2)]
    converted_amount = amount * conversion_rate

    response_data = {
        'currency1': currency1,
        'currency2': currency2,
        'amount': amount,
        'converted_to': converted_amount
    }
    return JsonResponse(response_data)
