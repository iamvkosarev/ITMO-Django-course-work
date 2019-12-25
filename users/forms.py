from django import forms
from hashlib import sha256
from json import loads, dump
from os import path
import json
from course_work.settings import BASE_DIR


class UserForm(forms.Form):
    # небязательное - required=False
    # user_id - задается программой
    first_name = forms.CharField()
    second_name = forms.CharField()
    patronymic = forms.CharField(required=False)
    birthday = forms.DateField()
    # status - Статут пользователь не задаёт
    # orders - Должен быть список, но пользователь его не задает
    login = forms.CharField()
    email = forms.CharField()
    phone_number = forms.CharField()
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    def hash_password(self):
        ret = super(UserForm, self).is_valid()
        self.cleaned_data["password1"] = sha256(self.cleaned_data["password1"].encode("ascii")).hexdigest()
        self.cleaned_data["password2"] = sha256(self.cleaned_data["password2"].encode("ascii")).hexdigest()

    def is_valid(self):
        ret = super(UserForm, self).is_valid()
        self.hash_password()
        errors = []
        login = self.cleaned_data["login"]
        email = self.cleaned_data["email"]
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        number = self.cleaned_data["phone_number"]
        if pass1 != pass2:
            errors.append("Пароли не совпадают")
        file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
        users = loads(file_json.read(), encoding='utf8')['users']
        file_json.close()
        for user in users:
            if user["login"] == login:
                errors.append("Пользователь с таким логином уже существует")
                break
        for user in users:
            if user["email"] == email:
                errors.append("Пользователь с такой электронной почтой уже существует")
                break
        for user in users:
            if user["phone_number"] == number:
                errors.append("Пользователь с таким номер телефона уже существует")
                break
        if len(errors) == 0:
            self.save()
            print("Добавлен пользователь")
        return errors

    def save(self):
        file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
        file_data = loads(file_json.read(), encoding='utf8')
        file_json.close()
        user_info = {"id": len(file_data["users"]),
                     "first_name": self.cleaned_data["first_name"],
                     "second_name": self.cleaned_data["second_name"],
                     "patronymic": self.cleaned_data["patronymic"],
                     "short_form": self.cleaned_data["second_name"] + " " +
                                   self.cleaned_data["first_name"] + "." +
                                   self.cleaned_data["patronymic"] + ".",
                     "birthday": self.cleaned_data["birthday"].strftime("%m.%d.%Y"),
                     "status": "just_user",
                     "orders": [],
                     "login": self.cleaned_data["login"],
                     "email": self.cleaned_data["email"],
                     "password": self.cleaned_data["password1"],
                     "phone_number": self.cleaned_data["phone_number"],
                     "reviews": []}
        file_data["users"].append(user_info)
        with open(path.join(BASE_DIR, "course_work\\data_base.json"), "w", encoding='utf8') as jsonFile:
            json.dump(file_data, jsonFile, ensure_ascii=False)


class LoginForm(forms.Form):
    login_or_email = forms.CharField()
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)

    def hash_password(self):
        ret = super(LoginForm, self).is_valid()
        self.cleaned_data["password"] = sha256(self.cleaned_data["password"].encode("ascii")).hexdigest()

    def is_valid(self):
        ret = super(LoginForm, self).is_valid()
        self.hash_password()
        return_data = {"error": "", "user": {}}
        login_or_email = self.cleaned_data["login_or_email"]
        password = self.cleaned_data["password"]
        file_json = open(path.join(BASE_DIR, "course_work\\data_base.json"), encoding="utf8")
        users = loads(file_json.read(), encoding='utf8')['users']
        file_json.close()
        for user in users:
            if user["login"] == login_or_email or user["email"] == login_or_email:
                if password == user["password"]:
                    return_data["user"] = user
                else:
                    return_data["error"] = "Неправильный пароль"
        if return_data["user"] == {} and return_data["error"] == "":
            return_data["error"] = "Пользователя с данным логином или почтой нет в базе данных"
        return return_data
