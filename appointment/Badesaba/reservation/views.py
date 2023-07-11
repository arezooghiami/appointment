from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient, Doctor, Appointment
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        doctor = get_object_or_404(Doctor, pk=pk)
        appointments = Appointment.objects.filter(doctor=doctor)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        doctor = get_object_or_404(Doctor, pk=pk)
        slots = []

        for i in range(7):
            date = (timezone.now().date() + timedelta(days=i)).strftime('%Y-%m-%d')
            appointments = Appointment.objects.filter(doctor=doctor, date=date)

            start_time = datetime.strptime('09:00', '%H:%M')
            end_time = datetime.strptime('17:00', '%H:%M')
            while start_time < end_time:
                slot_time = start_time.time()
                if not appointments.filter(time=slot_time).exists():
                    slots.append({'date': date, 'time': slot_time.strftime('%H:%M')})
                start_time += timedelta(minutes=30)

        return Response({'slots': slots})


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request):
        patient_number = request.data.get('mobile')
        doctor_id = request.data.get('doctor_id')
        date = request.data.get('date')
        time_string = request.data.get('time')
        time = datetime.strptime(time_string, '%H:%M:%S').time()

        if not patient_number:
            return Response({'status': 'failure', 'message': 'Mobile number is required.'})

        if not Patient.objects.filter(contact_info=patient_number).exists():
            return Response({'status': 'failure', 'message': 'Patient does not exist'})

        patient = Patient.objects.get(contact_info=patient_number)

        if not Doctor.objects.filter(id=doctor_id).exists():
            return Response({'status': 'failure', 'message': 'Doctor does not exist'})

        doctor = Doctor.objects.get(id=doctor_id)

        if Appointment.objects.filter(patient=patient, status='scheduled').exists():
            return Response({'status': 'failure', 'message': 'Patient already has an appointment'})

        if datetime.strptime(date, '%Y-%m-%d').date() < timezone.now().date():
            return Response({'status': 'failure', 'message': 'Cannot schedule appointment in the past'})

        start_time = datetime.strptime('09:00', '%H:%M').time()
        end_time = datetime.strptime('17:00', '%H:%M').time()
        if datetime.strptime(time_string, '%H:%M:%S').time() < start_time or datetime.strptime(time_string,
                                                                                               '%H:%M:%S').time() >= end_time:
            return Response({'status': 'failure', 'message': 'Appointment is outside working hours'})

        if Appointment.objects.filter(doctor=doctor, status='scheduled', date=date, time=time).exists():
            return Response({'status': 'failure', 'message': 'Doctor is not available at this time'})

        appointment = Appointment(patient=patient, doctor=doctor, date=date, time=time, status='scheduled')
        appointment.save()

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        patient_number = request.data.get('mobile')
        if not patient_number:
            return Response({'status': 'failure', 'message': 'Mobile number is required.'})

        if not Patient.objects.filter(contact_info=patient_number).exists():
            return Response({'status': 'failure', 'message': 'Patient not found.'})

        patient = Patient.objects.get(contact_info=patient_number)
        appointment = get_object_or_404(self.queryset, pk=pk, patient=patient)
        appointment.delete()
        return Response({'status': 'success', 'message': 'Appointment deleted.'})

    def list(self, request):
        patient_number = request.data.get('mobile')
        if not patient_number:
            return Response({'status': 'failure', 'message': 'Mobile number is required.'})

        if not Patient.objects.filter(contact_info=patient_number).exists():
            return Response({'status': 'failure', 'message': 'Patient not found.'})

        patient = Patient.objects.get(contact_info=patient_number)
        appointments = self.queryset.filter(patient=patient)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        patient_number = request.data.get('mobile')
        if not patient_number:
            return Response({'status': 'failure', 'message': 'Mobile number is required.'})

        if not Patient.objects.filter(contact_info=patient_number).exists():
            return Response({'status': 'failure', 'message': 'Patient not found.'})

        patient = Patient.objects.get(contact_info=patient_number)
        appointment = get_object_or_404(self.queryset, pk=pk, patient=patient)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)