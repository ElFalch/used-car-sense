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
    }

    return render(request, template, context)