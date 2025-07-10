#!/usr/bin/env python3
"""
Update test data to include completed service requests for rating testing
"""

import os
import sys
import django
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netfix.settings')
django.setup()

from services.models import ServiceRequest

def update_test_data():
    """Update some service requests to completed status"""
    print("Updating test data...")
    
    # Get first two service requests and mark them as completed
    requests = ServiceRequest.objects.all()[:2]
    
    for request in requests:
        request.status = 'completed'
        request.completion_date = timezone.now()
        request.save()
        print(f"✓ Marked request {request.id} as completed")
    
    print("Test data updated successfully!")

if __name__ == '__main__':
    update_test_data()
