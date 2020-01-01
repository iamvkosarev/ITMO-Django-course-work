from django.shortcuts import render
from django.http import HttpResponse
from os import path
from course_work.settings import BASE_DIR
from json import loads


def main_page(request):
    return render(request, 'main_page.html', {})


def find_users_organizations(id):
    users_organizations = []
    file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
    data = loads(file_json.read(), encoding='utf8')
    file_json.close()
    load_organizations_data(data)
    for organization in data["organizations"]:
        if id in organization["workers"]:
            users_organizations.append(organization)
    return users_organizations


def load_organizations_data(data):
    for organization in data['organizations']:
        director_id = organization["director_id"]
        for user in data["users"]:
            if user["id"] == director_id:
                organization["director_id"] = user["short_form"]
                break
        else:
            organization["director_id"] = "Отсутсвует"
