from django.shortcuts import render
from datetime import date

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    # fetches the customer user and all of the services requested by them
    user = User.objects.get(username=name)
    customer = Customer.objects.get(user=user)

    # Calculate age
    today = date.today()
    user_age = today.year - customer.birth.year - ((today.month, today.day) < (customer.birth.month, customer.birth.day))

    # Get all service requests for this customer
    service_requests = ServiceRequest.objects.filter(customer=customer).order_by("-request_date")

    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': user_age,
        'sh': service_requests
    })


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    company = Company.objects.get(user=user)
    services = Service.objects.filter(company=company).order_by("-date")

    # Get service requests for this company's services
    service_requests = ServiceRequest.objects.filter(
        service__company=company
    ).order_by("-request_date")

    return render(request, 'users/profile.html', {
        'user': user,
        'services': services,
        'service_requests': service_requests
    })
