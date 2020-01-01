from django.shortcuts import render, redirect, reverse
from organizations import forms
from json import loads
from os import path
from course_work.views import find_users_organizations
from course_work.settings import BASE_DIR
from course_work.views import load_organizations_data

def list(request):
    file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
    data = loads(file_json.read(), encoding='utf8')
    file_json.close()
    load_organizations_data(data)
    return render(request, 'organization/list.html', {"organizations": data['organizations']})


def dynamic_lookup_view(request, id):
    object = -1
    file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
    data = loads(file_json.read(), encoding='utf8')
    file_json.close()
    load_organizations_data(data)
    for organization in data["organizations"]:
        if id == organization["id"]:
            object = organization
    context = {"object": object, "id": id}
    if object != -1:
        return render(request, "organization/detail.html", context)
    else:
        return render(request, "organization/not_found.html", context)


def add(request):
    if "user" not in request.session:
        return redirect(reverse("main_page"))
    context = {"form": forms.OrganizationForm(),
               "errors": [],
               "form_is_not_ready": True,
               "id": -1}
    if request.method == "POST":
        data = forms.OrganizationForm(request.POST)
        context["form"] = forms.OrganizationForm(request.POST)
        return_data = data.is_valid(request.session["user"]["id"])
        if len(return_data["errors"]) > 0:
            context["errors"] = return_data["errors"]
        else:
            context["form_is_not_ready"] = False
            request.session["users_organizations"] = find_users_organizations(data["user"]["id"])
            context["id"] = return_data["id"]
    return render(request, "organization/add.html", context)
