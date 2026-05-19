from django.contrib import admin


from .models import TimeSlot
from .models import Appointment

admin.site.register(TimeSlot)
admin.site.register(Appointment)
