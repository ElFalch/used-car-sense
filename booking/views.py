from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from datetime import date

from .models import Appointment, TimeSlot

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = ["timeslot"]
    success_url = '/checkout/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # hide already booked slots
        booked_slots = Appointment.objects.values_list('timeslot_id', flat=True)
        form.fields['timeslot'].queryset = TimeSlot.objects.filter(day__gt=date.today()).exclude(id__in=booked_slots)  # noqa

        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        self.request.session['appointment_id'] = self.object.id

        return super().form_valid(form)

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "booking/my_bookings.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user).order_by(
            "timeslot__day", "timeslot__time"
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()

        return context

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ["timeslot"]
    template_name = "booking/edit_booking.html"
    success_url = reverse_lazy("my_bookings")

    def get_queryset(self):
        return Appointment.objects.filter(
            user=self.request.user,
            timeslot__day__gt=date.today()
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # exclude booked slots except current one
        booked_slots = Appointment.objects.exclude(
            id=self.object.id
        ).values_list('timeslot_id', flat=True)

        form.fields['timeslot'].queryset = TimeSlot.objects.filter(day__gt=date.today()).exclude(id__in=booked_slots)  # noqa
        return form

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "booking/delete_booking.html"
    success_url = reverse_lazy("my_bookings")

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)