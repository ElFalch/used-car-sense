from django.shortcuts import render, redirect
from .forms import ContactForm


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("contact")

    return render(request, "contact.html", {"form": form})
