from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Define URL pattern for the root path
    path('make_payment/', views.make_payment, name='make_payment'),
    path('counter/', views.counter, name='counter'),  # Added a trailing slash
    path('register/', views.register, name='register'),  # Added a trailing slash and comma
    path('login/', views.user_login, name='login'),  # Added a trailing slash and comma
    path('logout/', views.user_logout, name='logout'),  # Added a trailing slash and comma
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('request_payments/', views.request_payment, name='request_payments'),  # Added request_payment URL path
    path('view_accounts/', views.view_accounts, name='view_accounts'),  # Added view_accounts URL path
    path('user_accounts/', views.view_user_accounts, name='user_accounts'),
    path('all_transactions/', views.view_all_transactions, name='all_transactions'),
    path('success/', views.success, name='success'),  # Added success URL path
    path('notification/', views.notification, name='notification'),  # Added notification URL path
  
    path('handle_payment_request/<int:request_id>/<str:action>/', views.handle_payment_request, name='handle_payment_request'),


    # Add other URLs as needed
    # other URL patterns
]
