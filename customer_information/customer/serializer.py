from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class MedicalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalInformation
        fields = '__all__'
