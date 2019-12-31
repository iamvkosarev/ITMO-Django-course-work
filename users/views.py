from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from . import forms


def login(request):
    context = {"form": forms.LoginForm(),
         "error": "",
         "there_is_error": False}
    if "user" in request.session:
        return render(request, 'main_page.html', {})
    if request.method == "POST":
        obj = forms.LoginForm(request.POST)
        data = obj.is_valid()
        if data["error"] != "":
            context["error"] = data["error"]
            context["there_is_error"] = True
        else:
            request.session["user"] = data["user"]
            return redirect(reverse("main_page"))
    return render(request, 'user/login.html', context)


def logout(request):
    if "user" in request.session:
        del request.session["user"]
    return redirect(reverse("main_page"))


def registration(request):
    context = {"form": forms.UserForm(),
         "errors": [],
         "form_is_not_ready": True}
    if request.method == "POST":
        data = forms.UserForm(request.POST)
        context["form"] = forms.UserForm(request.POST)
        errors = data.is_valid()
        if len(errors) > 0:
            context["errors"] = errors
        else:
            context["form_is_not_ready"] = False
    return render(request, "user/registration.html", context)


def account(request):
    if "user" not in request.session:
        return render(request, 'main_page.html', {})
    return render(request, 'user/account.html', {"user": request.session["user"]})
