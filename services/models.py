from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    choices = (
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
    )
    field = models.CharField(max_length=30, blank=False,
                             null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    service_time = models.IntegerField()  # hours
    price = models.DecimalField(decimal_places=2, max_digits=100)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Rate this service from 1 to 5 stars"
    )
    review = models.TextField(blank=True, null=True, help_text="Optional review of the service")
    completion_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate total price based on service time and hourly rate
        self.price = self.service.price_hour * self.service_time
        super().save(*args, **kwargs)

        # Update service average rating when a rating is added
        if self.rating:
            self.update_service_rating()

    def update_service_rating(self):
        """Update the average rating for the service"""
        from django.db.models import Avg
        avg_rating = ServiceRequest.objects.filter(
            service=self.service,
            rating__isnull=False
        ).aggregate(Avg('rating'))['rating__avg']

        if avg_rating:
            self.service.rating = round(avg_rating)
            self.service.save()

    def can_be_rated(self):
        """Check if this service request can be rated"""
        return self.status == 'completed' and not self.rating

    def __str__(self):
        return f"{self.customer.user.username} - {self.service.name}"
