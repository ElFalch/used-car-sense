from django.shortcuts import render

# Create your views here.

from datetime import datetime, timedelta
from .models import Appointment
from django.views.generic import CreateView
from django.contrib import messages

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays

def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def booking(request):
    weekdays = validWeekday(200)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        day = request.POST.get('day')
        request.session['day'] = day

    return render(request,'booking/booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
        })

class BookingCreateView(CreateView):
    model = Appointment
    fields = ["day", "time"]
    
    def get_form(self, form_class=None):
        """Adds custom placeholders and widgets to form"""
        form = super().get_form(form_class)
        form.fields['day'].widget.attrs = {'type': 'day'}
        form.fields['time'].widget.attrs = {'type': 'time'}
        return form
    