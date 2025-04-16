# members/serializers.py
from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MemberRegistrationSerializer(serializers.ModelSerializer):
    # Aangepaste validators
    postal_code = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[1-9][0-9]{3}\s?[A-Z]{2}$',
                message='Voer een geldige Nederlandse postcode in (bijv. 1234 AB).'
            )
        ]
    )
    
    class Meta:
        model = Member
        fields = (
            'email', 'name', 'street', 'house_number', 'postal_code', 
            'city', 'phone', 'property_type', 'interest_solar', 
            'interest_battery', 'interest_sharing', 'interest_charger', 
            'interest_info_only', 'comments', 'newsletter'
        )
    
    def validate_email(self, value):
        # Controleer of email al bestaat
        if Member.objects.filter(email=value).exists():
            raise serializers.ValidationError("Dit e-mailadres is al geregistreerd.")
        return value
    
    def validate(self, data):
        # Ten minste één interesse moet geselecteerd zijn
        interests = [
            data.get('interest_solar', False),
            data.get('interest_battery', False),
            data.get('interest_sharing', False),
            data.get('interest_charger', False),
            data.get('interest_info_only', False)
        ]
        
        if not any(interests):
            raise serializers.ValidationError(
                {"interests": "Selecteer ten minste één interesse."}
            )
        
        return data