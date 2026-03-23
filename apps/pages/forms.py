from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Тема сообщения'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваше сообщение...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('subject', css_class='form-control'),
            Field('message', css_class='form-control'),
            Submit('submit', 'Отправить сообщение', css_class='btn btn-primary mt-3'),
        )
        self.helper.form_method = 'post'
