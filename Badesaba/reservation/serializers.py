from rest_framework import serializers
from .models import *

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'start_time', 'end_time', 'doctor', 'patient']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['__all__']