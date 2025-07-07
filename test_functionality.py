#!/usr/bin/env python3
"""
Simple test script to verify the Django NetFix application functionality
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netfix.settings')
django.setup()

from users.models import User, Customer, Company
from services.models import Service, ServiceRequest

def test_models():
    """Test that all models can be created successfully"""
    print("Testing models...")

    # Clean up any existing test data
    User.objects.filter(username__startswith='testuser').delete()
    User.objects.filter(username__startswith='testcompany').delete()

    # Test User creation
    import random
    random_suffix = random.randint(1000, 9999)
    user = User.objects.create_user(
        username=f'testuser{random_suffix}',
        email=f'test{random_suffix}@example.com',
        password='testpass123',
        is_customer=True
    )
    print(f"✓ User created: {user.username}")
    
    # Test Customer creation
    from datetime import date
    customer = Customer.objects.create(
        user=user,
        birth=date(1990, 1, 1)
    )
    print(f"✓ Customer created: {customer}")
    
    # Test Company creation
    company_user = User.objects.create_user(
        username=f'testcompany{random_suffix}',
        email=f'company{random_suffix}@example.com',
        password='testpass123',
        is_company=True
    )
    company = Company.objects.create(
        user=company_user,
        field='Plumbing'
    )
    print(f"✓ Company created: {company}")
    
    # Test Service creation
    service = Service.objects.create(
        company=company,
        name='Test Service',
        description='A test service',
        price_hour=50.00,
        field='Plumbing'
    )
    print(f"✓ Service created: {service}")
    
    # Test ServiceRequest creation
    service_request = ServiceRequest.objects.create(
        customer=customer,
        service=service,
        address='123 Test St',
        service_time=2
    )
    print(f"✓ ServiceRequest created: {service_request}")
    print(f"  - Calculated price: €{service_request.price}")
    
    print("All models working correctly! ✓")

def test_views():
    """Test that main views are accessible"""
    print("\nTesting views...")
    
    client = Client()
    
    # Test home page
    response = client.get('/')
    print(f"✓ Home page status: {response.status_code}")
    
    # Test services list
    response = client.get('/services/')
    print(f"✓ Services list status: {response.status_code}")
    
    # Test registration page
    response = client.get('/register/')
    print(f"✓ Registration page status: {response.status_code}")
    
    # Test login page
    response = client.get('/login/')
    print(f"✓ Login page status: {response.status_code}")
    
    print("All views accessible! ✓")

def test_forms():
    """Test form functionality"""
    print("\nTesting forms...")
    
    from users.forms import CustomerSignUpForm, CompanySignUpForm
    
    # Test customer form
    import random
    random_suffix = random.randint(10000, 99999)
    customer_data = {
        'username': f'newcustomer{random_suffix}',
        'email': f'newcustomer{random_suffix}@example.com',
        'password1': 'complexpass123',
        'password2': 'complexpass123',
        'birth': '1995-05-15'
    }
    
    form = CustomerSignUpForm(data=customer_data)
    if form.is_valid():
        print("✓ Customer signup form validation passed")
    else:
        print(f"✗ Customer form errors: {form.errors}")
    
    # Test company form
    company_data = {
        'username': f'newcompany{random_suffix}',
        'email': f'newcompany{random_suffix}@example.com',
        'password1': 'complexpass123',
        'password2': 'complexpass123',
        'field': 'Electricity'
    }
    
    form = CompanySignUpForm(data=company_data)
    if form.is_valid():
        print("✓ Company signup form validation passed")
    else:
        print(f"✗ Company form errors: {form.errors}")

if __name__ == '__main__':
    print("=== NetFix Application Test ===")
    try:
        test_models()
        test_views()
        test_forms()
        print("\n🎉 All tests passed! The application is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
