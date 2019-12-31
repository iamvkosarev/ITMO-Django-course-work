from django import forms
from course_work.settings import BASE_DIR
from json import loads, dump
from os import path
import json


class OrganizationForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=25)
    description = forms.CharField(min_length=15, max_length=100)
    date_of_foundation = forms.DateField()
    director_id = forms.CharField()
    TIN = forms.CharField(min_length=10, max_length=10)

    def is_valid(self):
        ret = super(OrganizationForm, self).is_valid()
        return_data = {"errors": []}
        name = self.cleaned_data["name"]
        TIN = self.cleaned_data["TIN"]
        director_id = int(self.cleaned_data["director_id"])
        file_json = open(path.join(BASE_DIR, "course_work/data_base.json"), encoding="utf8")
        data = loads(file_json.read(), encoding='utf8')
        file_json.close()
        for organization in data["organizations"]:
            if organization["name"] == name:
                return_data["errors"].append("Организация с таким названием уже существует")
            if organization["TIN"] == TIN:
                return_data["errors"].append("Организация с таким номером ИНН уже существует")
        for user in data["users"]:
            if user["id"] == director_id:
                break
        else:
            return_data["errors"].append("В базе данных отсутсвует пользователь с ID: {}".format(director_id))
        if len(return_data["errors"]) == 0:
            return_data["id"] = self.save()
        return return_data

    def save(self):
        file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
        file_data = loads(file_json.read(), encoding='utf8')
        file_json.close()
        organization_info = {"id": len(file_data["organizations"]),
                             "name": self.cleaned_data["name"],
                             "description": self.cleaned_data["description"],
                             "TIN": self.cleaned_data["TIN"],
                             "director_id": int(self.cleaned_data["director_id"]),
                             "date_of_foundation": self.cleaned_data["date_of_foundation"].strftime("%m.%d.%Y"),
                             "workers": [int(self.cleaned_data["director_id"])],
                             "reviews": [],
                             "completed_orders": [],
                             "topics": []
                             }
        file_data["organizations"].append(organization_info)
        with open(path.join(BASE_DIR, "course_work\\data_base.json"), "w", encoding='utf8') as jsonFile:
            json.dump(file_data, jsonFile, ensure_ascii=False)
        print("Добавлена организация: {}".format(organization_info["name"]))
        return organization_info["id"]
