from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer, Order, HealthRecord
from .serializer import CustomerSerializer, OrderSerializer, HealthRecordSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, HealthRecord, Order
from .serializer import CustomerSerializer, HealthRecordSerializer, OrderSerializer
from .frontend import *

# User Signup Send OTP
@api_view(['POST'])
def register_customer(request):
    
    name = request.data["name"]
    email = request.data["email"]
    phone_number = request.data["phoneNumber"]
    address = request.data["address"]
    date_of_birth = request.data["dateOfBirth"]
    gender = request.data["gender"]
    address = request.data["address"]
    
    try:
        cutomer = Customer.objects.get(mobile_number = phone_number, user_verified = True)
        return Response({"error" : "User already exist for the provided mobile number"}, status=status.HTTP_400_BAD_REQUEST)
    except Customer.DoesNotExist:
        pass
    except Exception as e:
        return Response({ "error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        Customer.objects.create(name = name, email = email, phone_number = phone_number, address = address, date_of_birth = date_of_birth, gender = gender )
    except Exception as e:
        return Response({ "error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"data" : "user created"}, status=status.HTTP_201_CREATED)


# User Signup Verify OTP
@api_view(['POST'])
def register_customer_otp_verify(request):
    
    phone_number = request.data["phoneNumber"]
    otp = request.data["otp"]
    
    try:
        cutomer = Customer.objects.get(mobile_number = phone_number)
        cutomer.user_verified = True
        cutomer.save()
    except Customer.DoesNotExist:
        return Response({"error" : "User does not exist for the provided mobile number"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({ "error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"data" : "user created"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def customer_login(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_health_record(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = HealthRecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def store_order_history(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
