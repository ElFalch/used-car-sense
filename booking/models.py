from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class TimeSlot(models.Model):
    day = models.DateField()
    time = models.CharField(max_length=10)

    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'time'], name='unique_timeslot')
        ]
        ordering = ['day', 'time']

    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"{self.day} | {self.time} ({status})"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return f"{self.user} | {self.timeslot.day} | {self.timeslot.time}"