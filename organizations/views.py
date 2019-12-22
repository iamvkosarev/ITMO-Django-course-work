from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from organizations import forms
from json import loads
from os import path
from course_work.settings import BASE_DIR


def list(request):
    with open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8") as file_json:
        data = loads(file_json.read(), encoding='utf8')['organizations']
        return render(request, 'list_of_organizations.html', {"organizations": data})
