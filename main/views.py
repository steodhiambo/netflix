from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.db.models import Count
from services.models import Service


def home(request):
    # Get top 5 most requested services for the home page
    top_services = Service.objects.annotate(
        request_count=Count('servicerequest')
    ).order_by('-request_count')[:5]

    return render(request, "main/home.html", {'top_services': top_services})


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
