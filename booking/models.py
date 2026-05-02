from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class TimeSlot(models.Model):
    day = models.DateField()
    time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'time'], name='unique_timeslot')
        ]
        ordering = ['day', 'time']

    def __str__(self):
        return f"{self.day} | {self.time}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    time_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} | {self.timeslot.day} | {self.timeslot.time}"