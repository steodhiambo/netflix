from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, datetime
from users.models import User, Customer, Company
from services.models import Service, ServiceRequest

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Create sample customers
        customer1_user = User.objects.create_user(
            username='john_doe',
            email='john@example.com',
            password='password123',
            is_customer=True
        )
        Customer.objects.create(user=customer1_user, birth=date(1990, 5, 15))

        customer2_user = User.objects.create_user(
            username='jane_smith',
            email='jane@example.com',
            password='password123',
            is_customer=True
        )
        Customer.objects.create(user=customer2_user, birth=date(1985, 8, 22))

        # Create sample companies
        company1_user = User.objects.create_user(
            username='plumbing_pro',
            email='plumbing@example.com',
            password='password123',
            is_company=True
        )
        company1 = Company.objects.create(user=company1_user, field='Plumbing')

        company2_user = User.objects.create_user(
            username='electric_experts',
            email='electric@example.com',
            password='password123',
            is_company=True
        )
        company2 = Company.objects.create(user=company2_user, field='Electricity')

        company3_user = User.objects.create_user(
            username='all_in_one_services',
            email='allinone@example.com',
            password='password123',
            is_company=True
        )
        company3 = Company.objects.create(user=company3_user, field='All in One')

        # Create sample services
        service1 = Service.objects.create(
            company=company1,
            name='Pipe Repair',
            description='Professional pipe repair and replacement services',
            price_hour=45.00,
            field='Plumbing'
        )

        service2 = Service.objects.create(
            company=company1,
            name='Drain Cleaning',
            description='Complete drain cleaning and unclogging services',
            price_hour=35.00,
            field='Plumbing'
        )

        service3 = Service.objects.create(
            company=company2,
            name='Electrical Wiring',
            description='Home and office electrical wiring installation',
            price_hour=55.00,
            field='Electricity'
        )

        service4 = Service.objects.create(
            company=company3,
            name='Home Cleaning',
            description='Complete home cleaning and maintenance',
            price_hour=25.00,
            field='Housekeeping'
        )

        service5 = Service.objects.create(
            company=company3,
            name='Garden Maintenance',
            description='Lawn mowing, trimming, and garden care',
            price_hour=30.00,
            field='Gardening'
        )

        # Create sample service requests
        customer1 = Customer.objects.get(user=customer1_user)
        customer2 = Customer.objects.get(user=customer2_user)

        ServiceRequest.objects.create(
            customer=customer1,
            service=service1,
            address='123 Main St, City',
            service_time=3
        )

        ServiceRequest.objects.create(
            customer=customer2,
            service=service1,
            address='456 Oak Ave, Town',
            service_time=2
        )

        ServiceRequest.objects.create(
            customer=customer1,
            service=service4,
            address='123 Main St, City',
            service_time=4
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data')
        )
