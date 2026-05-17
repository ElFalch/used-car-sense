from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['day', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
