from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . import forms


def login(request):
    d = {"form": forms.LoginForm(),
         "error": "",
         "there_is_error": False}
    if "user" in request.session:
        return render(request, 'main_page.html', {})
    if request.method == "POST":
        obj = forms.LoginForm(request.POST)
        data = obj.is_valid()
        if data["error"] != "":
            d["error"] = data["error"]
            d["there_is_error"] = True
        else:
            request.session["user"] = data["user"]
            return redirect(reverse("main_page"))
    return render(request, 'registration\login.html', d)


def logout(request):
    if "id" in request.session:
        del request.session["user"]
    return redirect(reverse("main_page"))


def registration(request):
    d = {"form": forms.UserForm(),
         "errors": [],
         "form_is_not_ready": True}
    if request.method == "POST":
        data = forms.UserForm(request.POST)
        d["form"] = forms.UserForm(request.POST)
        errors = data.is_valid()
        if len(errors) > 0:
            d["errors"] = errors
        else:
            d["form_is_not_ready"] = False
    return render(request, "registration\\registration.html", d)
