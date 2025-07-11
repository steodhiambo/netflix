from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_service_request_notification(service_request):
    """Send email notification when a service is requested"""
    try:
        # Email to company
        company_subject = f'New Service Request: {service_request.service.name}'
        company_context = {
            'service_request': service_request,
            'customer': service_request.customer,
            'service': service_request.service,
            'company': service_request.service.company,
        }
        
        company_html_message = render_to_string('emails/service_request_company.html', company_context)
        company_plain_message = strip_tags(company_html_message)
        
        send_mail(
            subject=company_subject,
            message=company_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[service_request.service.company.user.email],
            html_message=company_html_message,
            fail_silently=False,
        )
        
        # Email to customer (confirmation)
        customer_subject = f'Service Request Confirmation: {service_request.service.name}'
        customer_context = {
            'service_request': service_request,
            'customer': service_request.customer,
            'service': service_request.service,
            'company': service_request.service.company,
        }
        
        customer_html_message = render_to_string('emails/service_request_customer.html', customer_context)
        customer_plain_message = strip_tags(customer_html_message)
        
        send_mail(
            subject=customer_subject,
            message=customer_plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[service_request.customer.user.email],
            html_message=customer_html_message,
            fail_silently=False,
        )
        
        logger.info(f'Service request notification emails sent for request {service_request.id}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send service request notification emails: {str(e)}')
        return False


def send_status_update_notification(service_request, old_status, new_status):
    """Send email notification when service request status is updated"""
    try:
        subject = f'Service Request Status Update: {service_request.service.name}'
        context = {
            'service_request': service_request,
            'customer': service_request.customer,
            'service': service_request.service,
            'company': service_request.service.company,
            'old_status': old_status,
            'new_status': new_status,
        }
        
        html_message = render_to_string('emails/status_update.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[service_request.customer.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'Status update notification sent for request {service_request.id}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send status update notification: {str(e)}')
        return False


def send_service_completion_notification(service_request):
    """Send email notification when service is completed"""
    try:
        subject = f'Service Completed: {service_request.service.name}'
        context = {
            'service_request': service_request,
            'customer': service_request.customer,
            'service': service_request.service,
            'company': service_request.service.company,
        }
        
        html_message = render_to_string('emails/service_completed.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[service_request.customer.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'Service completion notification sent for request {service_request.id}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send service completion notification: {str(e)}')
        return False


def send_new_service_notification(service):
    """Send email notification to customers about new services (optional feature)"""
    try:
        # This could be used to notify customers about new services in their area
        # For now, we'll just log it as this would require customer preferences
        logger.info(f'New service created: {service.name} by {service.company.user.username}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to process new service notification: {str(e)}')
        return False


def send_rating_notification(service_request):
    """Send email notification to company when service is rated"""
    try:
        subject = f'Service Rated: {service_request.service.name}'
        context = {
            'service_request': service_request,
            'customer': service_request.customer,
            'service': service_request.service,
            'company': service_request.service.company,
        }
        
        html_message = render_to_string('emails/service_rated.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[service_request.service.company.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'Rating notification sent for request {service_request.id}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send rating notification: {str(e)}')
        return False
