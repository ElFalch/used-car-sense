from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order
from booking.models import Appointment

import stripe

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        appointment_data = request.session.get('appointment')

        if not appointment_data:
            messages.error(request, "You haven't chosen an appointment")
            return redirect('booking')
        
        appointment_obj = get_object_or_404(Appointment, id=appointment_data['id'])

        day = appointment_obj.timeslot.day
        time = appointment_obj.timeslot.time
        
        if not day:
            messages.error(request, "You haven't chosen an appointment")
            return redirect(reverse('booking'))

    stripe_total = 3000

    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'day': day,
        'time': time,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)

    appointment_data = request.session.get('appointment')

    if appointment_data:
        appointment_obj = Appointment.objects.get(id=appointment_data['id'])

        order.appointment = appointment_obj
        order.save()

        del request.session['appointment']

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)