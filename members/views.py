from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Member
from .serializers import MemberSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


from django.shortcuts import render

def test_form_view(request):
    return render(request, 'members/test_form.html')