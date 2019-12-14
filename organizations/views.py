from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from organizations import forms


def list(request):
    d = {"form": forms.OrganizationForm()}
    if request.method == "POST":
        d = forms.OrganizationForm(request.POST)
        if d.is_valid():
            pass
        return redirect(reverse('list'))
    return render(request, "list_of_organizations.html", d)