from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . import forms


def login(request):
    return render(request, 'registration\login.html', {})

def registration(request):
    d = {"form": forms.UserForm()}
    if request.method == "POST":
        d = forms.UserForm(request.POST)
        if d.is_valid():
            pass
        return redirect(reverse('registration'))
    return render(request, "registration\\registration.html", d)