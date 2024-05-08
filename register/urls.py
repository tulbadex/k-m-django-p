from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),  # Define URL pattern for the root path
    path('register', views.register, name='register'),  # Added a trailing slash and comma
    path('login', views.user_login, name='login'),  # Added a trailing slash and comma
    path('logout', views.user_logout, name='logout'),  # Added a trailing slash and comma

    # Add other URLs as needed
    # other URL patterns
]
