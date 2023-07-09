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
from .serializers import PatientSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
# from celery import shared_task
from django.utils import timezone
from .models import Appointment

# Create your views here.

#
# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     queryset = Appointment.objects.all()




class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# class AvailableAppointments(APIView):
#     def get(self, request, doctor_id, appointment_date):
#         doctor = Doctor.objects.get(id=doctor_id)
#         start_time = datetime.strptime(appointment_date, '%Y-%m-%d').date()
#         end_time = start_time + timedelta(days=1)
#         taken_appointments = Appointment.objects.filter(doctor=doctor, start_time__gte=start_time, end_time__lte=end_time).values_list('start_time', 'end_time')
#         available_appointments = []
#         current_time = start_time
#         while current_time < end_time:
#             if (current_time, current_time + timedelta(minutes=30)) not in taken_appointments:
#                 available_appointments.append((current_time, current_time + timedelta(minutes=30)))
#             current_time += timedelta(minutes=30)
#         return Response(available_appointments)



class AppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            patient_id = serializer.validated_data['patient_id']
            doctor_id = serializer.validated_data['doctor_id']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            patient = get_object_or_404(Patient, id=patient_id)
            doctor = get_object_or_404(Doctor, id=doctor_id)
            appointment = Appointment(patient=patient, doctor=doctor, date=date, time=time)
            appointment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DoctorAppointmentsListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Appointment.objects.filter(doctor_id=doctor_id)




# @shared_task
def send_reminders():
    appointments = Appointment.objects.filter(date__gte=timezone.now().date())
    for appointment in appointments:
        if (appointment.date - timezone.now().date()).days == 1:
            return Response({"message": "send reminder to patient and doctor"})
            #