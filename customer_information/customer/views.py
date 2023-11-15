from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import CustomerSerializer, OrderSerializer, HealthRecordSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, HealthRecord, Order
from .serializer import CustomerSerializer, HealthRecordSerializer, OrderSerializer
from .frontend import *
from .helper import *
from .imports import *
from .response_handler import *

# Save User details and Send OTP to verify its Phone number
class CustomerSignup(APIView):
    def post(self, request):

        name = request.data["name"]
        email = request.data["email"]
        phone_number = request.data["phone_number"]
        address = request.data["address"]
        date_of_birth = request.data["date_of_birth"]
        gender = request.data["gender"]

        try:
            customer = Customer.objects.get(phone_number = phone_number, user_verified = True )
            return WriteErrorMessageBadRequest("user already exist for the provided phone number")
        except Customer.DoesNotExist:
            Customer.objects.Create(name = name, email = email, phone_number = phone_number, address = address, date_of_birth = date_of_birth, gender = gender, medical_information_id = None )
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))

        return WriteSuccessMessage("otp sent to mobile number")
    
# Once user details are saved then OTP is sent to his number, which is verified using this API    
class VerifySignupOTP(APIView):
    def post(self, request):

        phone_number = request.data["phone_number"]
        otp = request.data["otp"]

        try:
            customer = Customer.objects.get(phone_number = phone_number, user_verified = False )
            if otp != "1111":
                return WriteErrorMessageBadRequest("Invalid OTP")
            customer.user_verified = True
            customer.save()
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobil number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))

        return WriteSuccessMessage("otp verified successfully")
    
# Allows for customer login and assigns a JWT token at time of login   
class CustomerLogin(APIView):
    def post(self, request):

        mobileNumber = request.data["mobileNumber"]

        try:
            customer = Customer.objects.get(phone_number = mobileNumber, user_verified = True )
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobil number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))
        
        data = serializers.serialize('json', [customer, ])
        customerData = json.loads(data)
        customerData = customerData[0]["fields"]

        jwtTokenResponse = NewGetJwtToken(mobileNumber)
        customerData["token"] = jwtTokenResponse["token"]

        return WriteSuccessMessageWithData(customerData)

# Update customer details in the record
class UpdateCustomerDetails(APIView):
    @transaction.atomic
    def post(self, request):

        jwtResponse = NewAuthenticateJWTtoken(request)
        validToken = jwtResponse["isValid"]
        if not validToken:
            return WriteErrorMessageBadRequest("Invalid Token passed")
        
        mobileNumber = jwtResponse["mobileNumber"]
        try:
            customer = Customer.objects.get(phone_number = mobileNumber, user_verified = True )
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobil number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))
        
        try:
            customer.name = request.data["name"] if "name" in request.data else customer.name
            customer.email = request.data["email"] if "email" in request.data else customer.email
            customer.phone_number = request.data["phone_number"] if "phone_number" in request.data else customer.phone_number
            customer.address = request.data["address"] if "address" in request.data else customer.address
            customer.date_of_birth = request.data["date_of_birth"] if "date_of_birth" in request.data else customer.date_of_birth
            customer.gender = request.data["gender"] if "gender" in request.data else customer.gender
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))

        customer.save()

        return WriteSuccessMessage("data has been save successfully")
    
# Remove Customer Record from the database    
class DeleteCustomerRecord(APIView):
    @transaction.atomic
    def post(self, request):
        jwtResponse = NewAuthenticateJWTtoken(request)
        validToken = jwtResponse["isValid"]
        if not validToken:
            return WriteErrorMessageBadRequest("Invalid Token passed")
        mobileNumber = jwtResponse["mobileNumber"]
        try:
            customer = Customer.objects.get(phone_number = mobileNumber, user_verified = True )
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobil number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))
        customer.delete()
        return WriteSuccessMessage("customer records removed")
    
# Allows you to added health details for the customer    
class AddHealthRecord(APIView):
    @transaction.atomic
    def post(self, request):

        jwtResponse = NewAuthenticateJWTtoken(request)
        validToken = jwtResponse["isValid"]
        if not validToken:
            return WriteErrorMessageBadRequest("Invalid Token passed")
        
        mobileNumber = jwtResponse["mobileNumber"]

        # Create new Health Record Entry

        medicalRecord = MedicalInformation.objects.create()

        medicalRecord.height = request.data["height"] if "height" in request.data else None
        medicalRecord.weight = request.data["weight"] if "weight" in request.data else None
        medicalRecord.blood_type = request.data["blood_type"] if "blood_type" in request.data else None
        medicalRecord.allergies = request.data["allergies"] if "allergies" in request.data else None
        medicalRecord.current_medications = request.data["current_medications"] if "current_medications" in request.data else None
        medicalRecord.blood_pressure = request.data["blood_pressure"] if "blood_pressure" in request.data else None
        medicalRecord.heart_rate = request.data["heart_rate"] if "heart_rate" in request.data else None

        medicalRecord.save()

        # Assign the Entry to the given customer
        try:
            customer = Customer.objects.get(phone_number = mobileNumber, user_verified = True )
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobile number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))
        
        customer.medical_information_id = medicalRecord.id
        customer.save()

        return WriteSuccessMessage("Health record added successfully")
    
# Allows for updating customer health record in the database    
class UpdateHealthRecord(APIView):
    def post(self, request):

        jwtResponse = NewAuthenticateJWTtoken(request)
        validToken = jwtResponse["isValid"]
        if not validToken:
            return WriteErrorMessageBadRequest("Invalid Token passed")
        
        mobileNumber = jwtResponse["mobileNumber"]

        # Find the Customer whose Health record has to be updated
        try:
            customer = Customer.objects.get(phone_number = mobileNumber, user_verified = True )
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobile number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))

        medicalRecord = MedicalInformation.objects.get(id = customer.medical_information_id)

        medicalRecord.height = request.data["height"] if "height" in request.data else medicalRecord.height
        medicalRecord.weight = request.data["weight"] if "weight" in request.data else medicalRecord.weight
        medicalRecord.blood_type = request.data["blood_type"] if "blood_type" in request.data else medicalRecord.blood_type
        medicalRecord.allergies = request.data["allergies"] if "allergies" in request.data else medicalRecord.allergies
        medicalRecord.current_medications = request.data["current_medications"] if "current_medications" in request.data else medicalRecord.current_medications
        medicalRecord.blood_pressure = request.data["blood_pressure"] if "blood_pressure" in request.data else medicalRecord.blood_pressure
        medicalRecord.heart_rate = request.data["heart_rate"] if "heart_rate" in request.data else medicalRecord.heart_rate

        medicalRecord.save()

        return WriteSuccessMessage("medical record for the customer has been updated successfully")
    
# Allows for removal of customer health record
class DeleteHealthRecord(APIView):
    def post(self, request):

        jwtResponse = NewAuthenticateJWTtoken(request)
        validToken = jwtResponse["isValid"]
        if not validToken:
            return WriteErrorMessageBadRequest("Invalid Token passed")
        
        mobileNumber = jwtResponse["mobileNumber"]

        # Find the Customer whose Health record has to be updated
        try:
            customer = Customer.objects.get(phone_number = mobileNumber, user_verified = True )
        except Customer.DoesNotExist:
            return WriteErrorMessageBadRequest("customer does not exist for the provided mobile number")
        except Exception as e:
            return WriteErrorMessageInternalServerError(str(e))

        medicalRecord = MedicalInformation.objects.get(id = customer.medical_information_id)
        medicalRecord.delete()
        customer.medical_information_id = None
        customer.save()

        return WriteSuccessMessage("customer health record has been deleted successfully")