from django.shortcuts import render

# Create your views here.

from .models import Appointment
from django.views.generic import CreateView


def booking(request):
    """ A view to return the index page """

    return render(booking, 'booking/appointment_form.html')


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = ["day", "time"]
    success_url = 'checkout'
    
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
        self.request.session['appointment'] = {'id': self.object.id, 'user': self.object.user.id}
        print(self.request.session['appointment'])
        return super().form_valid(form)
