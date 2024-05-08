from django.urls import path
from . import views

app_name = 'payapp'
urlpatterns = [
    path('', views.index, name='index'),  # Define URL pattern for the root path
    path('dashboard', views.dashboard, name='dashboard'),  # Define URL pattern for the root path
    path('make_payment', views.make_payment, name='make_payment'),
    path('counter', views.counter, name='counter'),  # Added a trailing slash
    path('view_transactions', views.view_transactions, name='view_transactions'),
    path('request_payments', views.request_payment, name='request_payments'),  # Added request_payment URL path
    path('view_accounts', views.view_accounts, name='view_accounts'),  # Added view_accounts URL path
    path('user_accounts', views.view_user_accounts, name='user_accounts'),
    path('all_transactions', views.view_all_transactions, name='all_transactions'),
    path('success', views.success, name='success'),  # Added success URL path
    path('notification', views.notification, name='notification'),  # Added notification URL path
  
    path('handle_payment_request/<int:request_id>/<str:action>', views.handle_payment_request, name='handle_payment_request'),

    path('conversion/<str:currency1>/<str:currency2>/<amount>', views.convert_currency, name='convert_currency'),

    # Add other URLs as needed
    # other URL patterns
]
