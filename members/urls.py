# members/urls.py
from django.urls import path
from . import views

app_name = 'members_app'  # Changed app_name to match the namespace

urlpatterns = [
    path('register/', views.register_member, name='register'),
    path('confirm-email/<str:token>/', views.confirm_email, name='confirm-email'),
]