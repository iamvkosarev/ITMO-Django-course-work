from django import forms


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
    phone_number = forms.IntegerField()
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    def is_valid(self):
        ret = super(UserForm, self).is_valid()
        self.save()
        return ret

    def save(self):
        print(self.cleaned_data)
