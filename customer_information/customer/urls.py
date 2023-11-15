from django.urls import path
from . import views
from . frontend import *
from .views import *

urlpatterns = [

    path('customer-signup', CustomerSignup.as_view(), name='customer'),
    path('customer-signup-verify-otp', VerifySignupOTP.as_view(), name='customer'),
    path('customer-login', CustomerLogin.as_view(), name='customer'),
    path('customer-update-details', UpdateCustomerDetails.as_view(), name='customer'),
    path('customer-delete-record', DeleteCustomerRecord.as_view(), name='customer'),

    path('add-health-record', AddHealthRecord.as_view(), name='healthRecord'),
    path('update-health-record', UpdateHealthRecord.as_view(), name='healthRecord'),
    path('delete-health-record', DeleteHealthRecord.as_view(), name='healthRecord')

]
