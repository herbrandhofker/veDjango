# Create your views here.
# members/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member
from .serializers import MemberSerializer, MemberRegistrationSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

def test_form_view(request):
    return render(request, 'members/test_form.html')

@api_view(['POST'])
def register_member(request):
    serializer = MemberRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Sla het lid op
        member = serializer.save()
        
        # Stel de vervaldatum van het token in (7 dagen vanaf nu)
        member.token_expiry = timezone.now() + timezone.timedelta(days=7)
        member.save()
        
        # Stuur bevestigingsmail
        send_confirmation_email(request, member)
        
        return Response({
            "status": "success",
            "message": "Registratie succesvol. Controleer uw e-mail voor de bevestigingslink."
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

def send_confirmation_email(request, member):
    """Stuur een bevestigingsmail naar het lid"""
    # Maak de bevestigingslink
    confirmation_path = reverse('confirm-email', kwargs={'token': member.confirmation_token})
    # Volledige URL maken (met domein)
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    domain = request.get_host()
    confirmation_url = f"{protocol}://{domain}{confirmation_path}"
    
    # Context voor de email templates
    context = {
        'member': member,
        'confirmation_url': confirmation_url,
    }
    
    # Render de email templates
    subject = "Bevestig uw aanmelding bij VerlichteEnergie"
    html_message = render_to_string('members/emails/confirmation_email.html', context)
    plain_message = render_to_string('members/emails/confirmation_email.txt', context)
    
    # Stuur de email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[member.email],
        html_message=html_message,
        fail_silently=False
    )

@api_view(['GET'])
def confirm_email(request, token):
    """Bevestig het e-mailadres van een lid via een token"""
    try:
        member = get_object_or_404(Member, confirmation_token=token)
        
        # Controleer of het token nog geldig is
        if not member.token_expiry or member.token_expiry < timezone.now():
            return Response({
                "status": "error",
                "message": "De bevestigingslink is verlopen. Neem contact op voor een nieuwe link."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Als het e-mailadres al is bevestigd
        if member.status != 'pending':
            return Response({
                "status": "info",
                "message": "Uw e-mailadres is al bevestigd.",
                "next_steps": "Log in om uw Tibber-account te koppelen."
            }, status=status.HTTP_200_OK)
        
        # Bevestig het e-mailadres
        member.status = 'confirmed'
        member.confirmation_date = timezone.now()
        member.save()
        
        return Response({
            "status": "success",
            "message": "Uw e-mailadres is succesvol bevestigd.",
            "next_steps": "Volg de instructies in de volgende e-mail om uw Tibber-account te koppelen."
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Er is een fout opgetreden bij het bevestigen van uw e-mailadres: {str(e)}"
        }, status=status.HTTP_400_BAD_REQUEST)