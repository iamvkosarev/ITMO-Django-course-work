from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . import forms


def login(request):
    return render(request, 'registration\login.html', {})


def registration(request):
    d = {"form": forms.UserForm(),
         "form_is_not_correct": True,
         "errors": []}
    if request.method == "POST":
        data = forms.UserForm(request.POST)
        d["form"] = forms.UserForm(request.POST)
        errors = data.is_valid()
        if len(errors):
            d["errors"] = errors
        else:
            d["form_is_not_correct"] = False
    return render(request, "registration\\registration.html", d)
