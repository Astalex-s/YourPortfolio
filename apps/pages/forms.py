import time

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot: hidden field that should remain empty (bots fill it)
    website = forms.CharField(required=False, widget=forms.HiddenInput())
    # Timestamp to detect too-fast submissions
    form_loaded_at = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'telegram_username', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'telegram_username': forms.TextInput(attrs={'placeholder': '@username'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Тема сообщения'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваше сообщение...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telegram_username'].required = True
        self.fields['form_loaded_at'].initial = str(int(time.time()))
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('telegram_username', css_class='form-control'),
            Field('subject', css_class='form-control'),
            Field('message', css_class='form-control'),
            Submit('submit', 'Отправить сообщение', css_class='btn btn-primary mt-3'),
        )
        self.helper.form_method = 'post'

    def clean_website(self):
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError('Обнаружена подозрительная активность.')
        return value

    def clean_form_loaded_at(self):
        loaded_at = self.cleaned_data.get('form_loaded_at', '')
        try:
            loaded_ts = int(loaded_at)
        except (ValueError, TypeError):
            raise forms.ValidationError('Ошибка валидации формы.')
        elapsed = int(time.time()) - loaded_ts
        if elapsed < 3:
            raise forms.ValidationError('Форма отправлена слишком быстро. Попробуйте снова.')
        return loaded_at

    def clean_telegram_username(self):
        value = self.cleaned_data.get('telegram_username', '').strip()
        if not value:
            raise forms.ValidationError('Укажите ваш Telegram аккаунт.')
        # Normalize: add @ if missing
        if not value.startswith('@'):
            value = '@' + value
        # Validate format: @username (5-32 chars, alphanumeric + underscores)
        username = value[1:]
        if len(username) < 4 or len(username) > 32:
            raise forms.ValidationError('Telegram username должен быть от 4 до 32 символов.')
        if not all(c.isalnum() or c == '_' for c in username):
            raise forms.ValidationError('Telegram username может содержать только буквы, цифры и подчёркивания.')
        return value
