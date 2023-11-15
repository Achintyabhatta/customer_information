from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer
from .serializer import CustomerSerializer

class CustomerAPITest(APITestCase):
    def test_register_customer(self):
        url = reverse('register_customer')
        data = {'name': 'Test Customer', 'email': 'test@example.com', 'phone_number': '1234567890', 'address': 'Test Address'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_health_record(self):
        customer = Customer.objects.create(name='Test Customer', email='test@example.com', phone_number='1234567890', address='Test Address')
        url = reverse('add_health_record', kwargs={'customer_id': customer.id})
        data = {'customer': customer.id, 'height': 170, 'weight': 70, 'blood_type': 'O+', 'allergies': 'Pollen', 'current_medications': 'None'}
        response = self.client.post(url, data, format='json')
        print(response.data)  # Print the response data for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Expected status code 201")

    def test_store_order_history(self):
        customer = Customer.objects.create(name='Test Customer', email='test@example.com', phone_number='1234567890', address='Test Address')
        url = reverse('store_order_history', kwargs={'customer_id': customer.id})
        data = {'customer': customer.id, 'total_amount': 100.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
