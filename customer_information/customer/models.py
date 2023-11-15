from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key = True)
    created_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    user_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    medical_information_id = models.IntegerField()
    gender = models.TextField(default="M")

    def __str__(self):
        return self.name

class MedicalInformation(models.Model):
    id = models.AutoField(primary_key = True)
    created_at = models.DateTimeField(auto_now=True)
    height = models.FloatField()
    weight = models.FloatField()
    blood_type = models.CharField(max_length=5)
    allergies = models.TextField()
    current_medications = models.TextField()
    blood_pressure = models.IntegerField()
    heart_rate = models.IntegerField()

    def __str__(self):
        return self.name