from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50)
    expertis=models.TextField()
    phone = models.IntegerField()
    def __str__(self):
        return self.fullname




class Patient(models.Model):
    SEX=[
        ('male','male'),
        ('femail','female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10,choices=SEX,default='male')
    phone = models.IntegerField(null=True,blank=True)
    history=models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    # دیگر فیلدهای مورد نیاز

class Appointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.doctor} - {self.patient}"





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