from django.shortcuts import render

def home(request):
    return render(request, 'website/home.html')

def aanmelden(request):
    return render(request, 'website/aanmelden.html')