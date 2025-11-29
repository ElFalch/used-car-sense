from django.db import models
from datetime import datetime, timedelta 
from django.contrib.auth.models import User

# Create your models here.
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)


DATE_CHOICES = (
    (str(datetime.now() + timedelta(1)), str(datetime.now() + timedelta(1))),
    (str(datetime.now() + timedelta(2)), str(datetime.now() + timedelta(2))),
    (str(datetime.now() + timedelta(3)), str(datetime.now() + timedelta(3))),
    (str(datetime.now() + timedelta(4)), str(datetime.now() + timedelta(4))),
    (str(datetime.now() + timedelta(5)), str(datetime.now() + timedelta(5))),
)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    day = models.CharField(max_length=26, choices=DATE_CHOICES, default= datetime.now() + timedelta(1))
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default= "3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"