from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AppointmentSerializer
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework import viewsets
from .models import Patient
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
# from celery import shared_task
from django.utils import timezone
from .models import Appointment
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']

            # Check if start_time and end_time are valid
            if start_time < timezone.now():
                return Response({'error': 'Invalid start time'}, status=status.HTTP_400_BAD_REQUEST)
            if end_time < start_time:
                return Response({'error': 'Invalid end time'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if doctor is available at the requested time
            appointments = Appointment.objects.filter(doctor=doctor, start_time__gte=start_time - timedelta(minutes=30),
                                                      end_time__lte=end_time + timedelta(minutes=30))

            if appointments.exists():
                return Response({'error': 'Doctor is not available at the requested time'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Create the appointment if everything is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class DoctorAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Appointment.objects.filter(doctor_id=doctor_id)


class PatientAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Appointment.objects.filter(patient_id=patient_id)


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

