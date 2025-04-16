from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
import uuid

class Member(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Aanmelding ontvangen'),
        ('confirmed', 'E-mail bevestigd'),
        ('tibber_connected', 'Tibber gekoppeld'),
        ('active', 'Actief'),
        ('inactive', 'Inactief'),
    ]
    
    PROPERTY_CHOICES = [
        ('huurwoning', 'Huurwoning'),
        ('koopwoning', 'Koopwoning'),
        ('kantoor', 'Kantoor'),
        ('koepel', 'Koepel'),
        ('tm-centrum', 'TM-centrum'),
        ('anders', 'Anders'),
    ]
    
    # Basisgegevens
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    
    # Adresgegevens
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100, default='Lelystad')
    
    # Contactgegevens
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Eigenschappen
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES)
    
    # Interesses
    interest_solar = models.BooleanField(default=False)
    interest_battery = models.BooleanField(default=False)
    interest_sharing = models.BooleanField(default=False)
    interest_charger = models.BooleanField(default=False)
    interest_info_only = models.BooleanField(default=False)
    
    # Voorkeuren
    comments = models.TextField(blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    
    # Status en Tibber-integratie
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tibber_token = models.CharField(max_length=255, blank=True, null=True)
    
    # Tijdstippen
    registration_date = models.DateTimeField(auto_now_add=True)
    confirmation_date = models.DateTimeField(blank=True, null=True)
    activation_date = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Beveiliging
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    token_expiry = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def set_token_expiry(self):
        """Set token expiry to 7 days from now"""
        self.token_expiry = timezone.now() + timezone.timedelta(days=7)
        self.save(update_fields=['token_expiry'])
    
    def confirm_email(self):
        """Mark email as confirmed"""
        self.status = 'confirmed'
        self.confirmation_date = timezone.now()
        self.save(update_fields=['status', 'confirmation_date'])
    
    def connect_tibber(self, token):
        """Connect Tibber account"""
        self.tibber_token = token
        self.status = 'tibber_connected'
        self.save(update_fields=['tibber_token', 'status'])
    
    def activate(self):
        """Activate member"""
        self.status = 'active'
        self.activation_date = timezone.now()
        self.save(update_fields=['status', 'activation_date'])
    
    def deactivate(self):
        """Deactivate member"""
        self.status = 'inactive'
        self.save(update_fields=['status'])
    
    def is_token_valid(self):
        """Check if confirmation token is still valid"""
        return self.token_expiry and self.token_expiry > timezone.now()