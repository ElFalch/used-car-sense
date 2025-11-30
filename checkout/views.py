from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    appointment = request.session.get('appointment', {})
    if not appointment:
        messages.error(request, "You haven't chosen an appointment")
        return redirect(reverse('booking'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)