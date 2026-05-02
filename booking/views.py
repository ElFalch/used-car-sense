from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.urls import reverse_lazy   
from django.views.generic import DeleteView                                                                                                                                                                                                                                                              

# Create your views here.

from .models import Appointment
from django.views.generic import CreateView


def booking(request):
    """ A view to return the index page """

    return render(booking, 'booking/appointment_form.html')


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = ["day", "time"]
    success_url = '/checkout/'
    
    def get_form(self, form_class=None):
        """Adds custom placeholders and widgets to form"""
        form = super().get_form(form_class)
        form.fields['day'].widget.attrs = {'type': 'day'}
        form.fields['time'].widget.attrs = {'type': 'time'}
        return form
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        self.request.session['appointment'] = {
        'day': self.object.day,
        'time': self.object.time,
        'id': self.object.id
        }
        return super().form_valid(form)


class MyBookingsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "booking/my_bookings.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user).order_by("day", "time")


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ["day", "time"]
    template_name = "booking/edit_booking.html"
    success_url = reverse_lazy("my_bookings")

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "booking/delete_booking.html"
    success_url = reverse_lazy("my_bookings")

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)        