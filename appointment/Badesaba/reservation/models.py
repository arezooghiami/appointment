from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_info = models.CharField(max_length=100)
    medical_history = models.TextField()

    def __str__(self):
        return str(self.id)


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'scheduled'

        newdate = datetime.datetime.strptime(self.date, '%Y-%m-%d').date()

        if newdate < timezone.now().date() or (newdate == timezone.now().date() and self.time < timezone.now().time()):
            self.status = 'completed'

        super().save(*args, **kwargs)

# class Doctor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     fullname = models.CharField(max_length=50)
#     expertis=models.TextField()
#     phone = models.IntegerField()
#     def __str__(self):
#         return self.fullname
#
#
#
#
# class Patient(models.Model):
#     SEX=[
#         ('male','male'),
#         ('femail','female')
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     age = models.PositiveIntegerField()
#     sex = models.CharField(max_length=10,choices=SEX,default='male')
#     phone = models.IntegerField(null=True,blank=True)
#     history=models.TextField()
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return self.name
#
#
#
# class Appointment(models.Model):
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(default=timezone.now)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"{self.doctor} - {self.patient}"
#
#     def end_time(self):
#         return self.start_time + timedelta(minutes=30)
#
#     def save(self, *args, **kwargs):
#         self.end_time_calculated = self.end_time()
#         super().save(*args, **kwargs)
#
#



# class Appointment(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.patient} with {self.doctor} on {self.date} at {self.time}"
#
#     def is_past_due(self):
#         return timezone.now() > timezone.datetime.combine(self.date, self.time)