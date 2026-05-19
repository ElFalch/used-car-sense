from django.db import models
from django.contrib.auth.models import User


class TimeSlot(models.Model):
    day = models.DateField()
    time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['day', 'time'],
                name='unique_timeslot',
            ),
        ]
        ordering = ['day', 'time']

    def __str__(self):
        return f"{self.day} | {self.time}"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    time_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending Payment"),
            ("confirmed", "Confirmed"),
        ],
        default="pending"
    )
    
    def __str__(self):
        return f"{self.user} | {self.timeslot}"