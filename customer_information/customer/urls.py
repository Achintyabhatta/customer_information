from django.urls import path
from . import views
from . frontend import *

urlpatterns = [
    path('register/', views.register_customer, name='register_customer'),
    path('add-health-record/<int:customer_id>/', views.add_health_record, name='add_health_record'),
    path('store-order-history/<int:customer_id>/', views.store_order_history, name='store_order_history'),
    path('customer/', Home , name='customer'),
]
