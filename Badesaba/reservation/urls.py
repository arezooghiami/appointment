# from rest_framework import routers
# from .views import PatientViewSet
# from django.urls import path
# from .views import DoctorAppointmentsListView
from django.urls import path, include
from .views import *
#
# router = routers.DefaultRouter()
# router.register(r'patients', PatientViewSet)
# router.register(r'doctors', DoctorViewSet)
#
# urlpatterns = router.urls


urlpatterns = [
    path('',AppointmentCreateView.as_view()),
]