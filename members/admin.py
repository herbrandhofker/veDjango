# Register your models here.
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'postal_code', 'property_type', 'status', 'registration_date')
    list_filter = ('status', 'property_type', 'interest_solar', 'interest_battery', 
                  'interest_sharing', 'interest_charger', 'newsletter')
    search_fields = ('name', 'email', 'postal_code', 'comments')
    readonly_fields = ('registration_date', 'confirmation_date', 'activation_date', 
                      'last_updated', 'confirmation_token')
    
    fieldsets = (
        ('Persoonlijke informatie', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Adresgegevens', {
            'fields': ('street', 'house_number', 'postal_code', 'city')
        }),
        ('Eigenschappen en interesses', {
            'fields': (
                'property_type', 
                ('interest_solar', 'interest_battery', 'interest_sharing', 'interest_charger', 'interest_info_only'),
                'comments', 
                'newsletter'
            )
        }),
        ('Status en Tibber', {
            'fields': ('status', 'tibber_token')
        }),
        ('Tijdstippen', {
            'fields': ('registration_date', 'confirmation_date', 'activation_date', 'last_updated'),
            'classes': ('collapse',)
        }),
        ('Beveiliging', {
            'fields': ('confirmation_token', 'token_expiry'),
            'classes': ('collapse',)
        }),
    )