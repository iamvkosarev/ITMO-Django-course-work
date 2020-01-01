from django.shortcuts import render, redirect, reverse
from organizations import forms
from json import loads
from os import path
from course_work.views import find_users_organizations
from course_work.settings import BASE_DIR
from course_work.views import load_organizations_data


def list(request):
    return render(request, 'order/list.html', {})


def dynamic_lookup_view(request, id):
    object = -1
    context = {"object": object, "id": id}
    if object != -1:
        return render(request, "order/detail.html", context)
    else:
        return render(request, "order/not_found.html", context)


def add(request):
    if "user" not in request.session:
        return redirect(reverse("main_page"))
    context = {"form": forms.OrganizationForm(),
               "errors": [],
               "form_is_not_ready": True,
               "id": -1}
    return render(request, "order/add.html", context)
