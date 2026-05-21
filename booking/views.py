from django.contrib import messages
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
        booked_slots = Appointment.objects.values_list(
            'timeslot_id',
            flat=True)
        form.fields['timeslot'].queryset = TimeSlot.objects.filter(
            day__gt=date.today()).exclude(id__in=booked_slots)

        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        self.request.session['appointment_id'] = self.object.id

        messages.success(
            self.request,
            "Your appointment has been selected!"
            "Please fill out the form below to confirm this booking"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was a problem booking your appointment. Please try again."
        )
        return super().form_invalid(form)


class MyBookingsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "booking/my_bookings.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(
            user=self.request.user, status="confirmed").order_by(
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

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your booking has been updated successfully."
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Unable to update your booking."
            "Please check the form and try again."
        )

        return super().form_invalid(form)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "booking/delete_booking.html"
    success_url = reverse_lazy("my_bookings")

    def get_queryset(self):
        return Appointment.objects.filter(
            user=self.request.user,
            timeslot__day__gt=date.today()
        )

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "Your booking has been cancelled successfully."
        )
        return super().delete(request, *args, **kwargs)