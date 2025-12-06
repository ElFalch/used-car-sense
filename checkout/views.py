from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    day = request.session.get('day', {});
    time = request.session.get('time', {});
    if not day:
        messages.error(request, "You haven't chosen an appointment")
        return redirect(reverse('booking'))
    print(day)
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'day': day,
        'time': time,
        'stripe_public_key': 'pk_test_51SbNQP14T0kXCw0Oz2xjNqfZeTheSPlrM80RP4IstANuREGeSwl0ADUxRZGLyOw412KgkAckZ3v1SKS2s6kbco7L00TU0cxMsl',
    }

    return render(request, template, context)