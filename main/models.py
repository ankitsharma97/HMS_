from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    department = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/Doctor/', null=True, blank=True)
    
    def __str__(self):
        return self.name    
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    address = models.CharField(max_length=100, null=True, blank=True,default='')   
    pin_code = models.CharField(max_length=10, null=True, blank=True,default='')
    mobile_number = models.CharField(max_length=15, null=True, blank=True,default='')
    
    def __str__(self):
        return self.name
  
class Status(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,default=1)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} on {self.date}"
    
class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    report = models.FileField(upload_to='patient_report/')
    date = models.DateField()
    
    def __str__(self):
        return f"Report for {self.patient.name} by {self.doctor.name} on {self.date}"
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class TreatmentPlan(models.Model):
    name = models.CharField(max_length=100, default='Treatment Plan')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    spending = models.FloatField(default=0) 
    description = models.TextField()

    def __str__(self):
        return self.name

class History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    date = models.DateField()
    
    def __str__(self):
        return f"History for {self.patient.name} - {self.disease} on {self.date}"


class WoundHealing(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    photos = models.ImageField(upload_to='wound_photos/')
    

    def __str__(self):
        return f"Wound Healing for {self.patient.username} on {self.date}"
    
class Polls(models.Model):
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    def __str__(self):
        return self.question
    

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    def __str__(self):
        return self.answer