from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm

import stripe

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    day = request.session.get('day', {});
    time = request.session.get('time', {});
    if not day:
        messages.error(request, "You haven't chosen an appointment")
        return redirect(reverse('booking'))

    stripe_total = 20
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'day': day,
        'time': time,
        'stripe_public_key': 'pk_test_51SbNQP14T0kXCw0Oz2xjNqfZeTheSPlrM80RP4IstANuREGeSwl0ADUxRZGLyOw412KgkAckZ3v1SKS2s6kbco7L00TU0cxMsl',
    }

    return render(request, template, context)