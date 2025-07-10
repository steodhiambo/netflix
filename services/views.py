from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg

from users.models import Company, Customer, User

from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm, RateServiceForm


def service_list(request):
    # Get all services
    services = Service.objects.all().order_by("-date")

    # Pagination
    paginator = Paginator(services, 8)  # Show 8 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services/list.html', {
        'services': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


def most_requested(request):
    # Get services ordered by number of requests
    from django.db.models import Count
    services = Service.objects.annotate(
        request_count=Count('servicerequest')
    ).order_by('-request_count')
    return render(request, 'services/most_requested.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    if not request.user.is_company:
        messages.error(request, 'Only companies can create services.')
        return redirect('/')

    company = Company.objects.get(user=request.user)

    # Define available choices based on company field
    if company.field == 'All in One':
        choices = [
            ('Air Conditioner', 'Air Conditioner'),
            ('Carpentry', 'Carpentry'),
            ('Electricity', 'Electricity'),
            ('Gardening', 'Gardening'),
            ('Home Machines', 'Home Machines'),
            ('Housekeeping', 'Housekeeping'),
            ('Interior Design', 'Interior Design'),
            ('Locks', 'Locks'),
            ('Painting', 'Painting'),
            ('Plumbing', 'Plumbing'),
            ('Water Heaters', 'Water Heaters'),
        ]
    else:
        choices = [(company.field, company.field)]

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            service = Service.objects.create(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=form.cleaned_data['field']
            )
            messages.success(request, 'Service created successfully!')
            return redirect('services_list')
    else:
        form = CreateNewService(choices=choices)

    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


@login_required
def request_service(request, id):
    if not request.user.is_customer:
        messages.error(request, 'Only customers can request services.')
        return redirect('/')

    service = get_object_or_404(Service, id=id)
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            service_request = ServiceRequest.objects.create(
                customer=customer,
                service=service,
                address=form.cleaned_data['address'],
                service_time=form.cleaned_data['service_time']
            )
            messages.success(request, 'Service requested successfully!')
            return redirect('index', id=service.id)
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })


@login_required
def rate_service(request, request_id):
    if not request.user.is_customer:
        messages.error(request, 'Only customers can rate services.')
        return redirect('/')

    service_request = get_object_or_404(ServiceRequest, id=request_id, customer__user=request.user)

    if not service_request.can_be_rated():
        messages.error(request, 'This service cannot be rated.')
        return redirect('customer_profile', name=request.user.username)

    if request.method == 'POST':
        form = RateServiceForm(request.POST)
        if form.is_valid():
            service_request.rating = int(form.cleaned_data['rating'])
            service_request.review = form.cleaned_data['review']
            service_request.save()
            messages.success(request, 'Thank you for rating this service!')
            return redirect('customer_profile', name=request.user.username)
    else:
        form = RateServiceForm()

    return render(request, 'services/rate_service.html', {
        'form': form,
        'service_request': service_request
    })


def update_request_status(request, request_id):
    """Allow companies to update service request status"""
    if not request.user.is_company:
        messages.error(request, 'Only companies can update request status.')
        return redirect('/')

    service_request = get_object_or_404(ServiceRequest, id=request_id, service__company__user=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in_progress', 'completed', 'cancelled']:
            service_request.status = new_status
            if new_status == 'completed':
                from django.utils import timezone
                service_request.completion_date = timezone.now()
            service_request.save()
            messages.success(request, f'Request status updated to {new_status}.')

    return redirect('company_profile', name=request.user.username)
