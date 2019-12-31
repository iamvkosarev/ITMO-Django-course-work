from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from organizations import forms
from json import loads
from os import path
from course_work.settings import BASE_DIR


def list(request):
    file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
    data = loads(file_json.read(), encoding='utf8')
    file_json.close()
    for organization in data['organizations']:
        director_id = organization["director_id"]
        for user in data["users"]:
            if user["id"] == director_id:
                organization["director_id"] = user["short_form"]
                break
        else:
            organization["director_id"] = "Отсутсвует"
    return render(request, 'organization/list.html', {"organizations": data['organizations']})


def dynamic_lookup_view(request, id):
    object = -1
    file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
    organizations = loads(file_json.read(), encoding='utf8')['organizations']
    file_json.close()
    for organization in organizations:
        if id == organization["id"]:
            object = organization
    context = {"object": object, "id": id}
    if object != -1:
        return render(request, "organization/detail.html", context)
    else:
        return render(request, "organization/not_found.html", context)


def add(request):
    if "user" not in request.session:
        return render(request, 'main_page.html', {})
    context = {"form": forms.OrganizationForm(),
               "errors": [],
               "form_is_not_ready": True,
               "id": -1}
    if request.method == "POST":
        data = forms.OrganizationForm(request.POST)
        context["form"] = forms.OrganizationForm(request.POST)
        return_data = data.is_valid()
        if len(return_data["errors"]) > 0:
            context["errors"] = return_data["errors"]
        else:
            context["form_is_not_ready"] = False
            context["id"] = return_data["id"]
    return render(request, "organization/add.html", context)
