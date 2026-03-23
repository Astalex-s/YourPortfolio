from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import UserProfile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Field('username'),
            Field('email'),
            Field('password1'),
            Field('password2'),
            Submit('submit', 'Зарегистрироваться', css_class='btn btn-primary mt-3 w-100'),
        )


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=150, required=False, label='Фамилия')

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Field('bio'),
            Field('avatar'),
            Submit('submit', 'Сохранить', css_class='btn btn-primary mt-3'),
        )
