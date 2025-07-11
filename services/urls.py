from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.service_list, name='services_list'),
    path('create/', v.create, name='services_create'),
    path('search/', v.search_services, name='search_services'),
    path('most-requested/', v.most_requested, name='most_requested'),
    path('request/<int:request_id>/rate/', v.rate_service, name='rate_service'),
    path('request/<int:request_id>/update-status/', v.update_request_status, name='update_request_status'),
    path('<int:id>', v.index, name='index'),
    path('<int:id>/request_service/', v.request_service, name='request_service'),
    path('<slug:field>/', v.service_field, name='services_field'),
]
