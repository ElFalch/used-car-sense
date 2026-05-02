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
    day = models.CharField(max_length=26, choices=DATE_CHOICES)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
 # Uniqueness protection taken from: https://stackoverflow.com/questions/57149015/creating-a-models-uniqueconstraint-in-abstract-model   
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day', 'time'], name='unique_day_time')
        ]