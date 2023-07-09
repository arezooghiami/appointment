
from django.urls import path
from .views import *

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patients_list'),
    path('doctors/', DoctorListView.as_view(), name='doctors_list'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointments_list_create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointments_detail'),
    path('doctors/<int:doctor_id>/appointments/', DoctorAppointmentsListView.as_view(), name='doctor_appointments_list'),
    path('patients/<int:patient_id>/appointments/', PatientAppointmentsListView.as_view(), name='patient_appointments_list'),
]