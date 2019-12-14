from django import forms


class OrganizationForm(forms.Form):
    title = forms.CharField(max_length=30)
    director = forms.CharField(max_length=50)

    def is_valid(self):
        ret = super(OrganizationForm, self).is_valid()
        self.save()
        return ret

    def save(self):
        print(self.cleaned_data['title'])