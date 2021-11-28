from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.forms import ModelForm

from . import models

User = get_user_model()


class LoginForm(AuthenticationForm):
    """- Форма авторизации"""

    username = UsernameField(
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'autocomplete': 'off'
        })
    )

    password = forms.CharField(
        initial='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'off'
        })
    )

    def clean_username(self):
        """- проверка почты на валидность"""
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).first():
            raise forms.ValidationError("Пользователь не найден.")
        return username

    def clean_password(self):
        """- проверка пароля на валидность"""
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username)
        for u in user:
            if not check_password(password, u.password):
                raise forms.ValidationError("Не верный пароль")
        return password

    class Meta:
        model = User
        fields = ('username', 'password')


class CreateArticleForm(ModelForm):
    """- Форма создания новой статьи"""

    title = forms.CharField(
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Заголовок',
            'autocomplete': 'off'
        })
    )

    description = forms.CharField(
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Описание',
            'autocomplete': 'off'
        })
    )

    content = forms.CharField(
        initial='',
        widget=forms.Textarea(attrs={
            'cols': 60,
            'rows': 10,
            'class': 'form-control',
            'placeholder': 'Содержание',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = models.Article
        fields = ('title', 'description', 'content')

