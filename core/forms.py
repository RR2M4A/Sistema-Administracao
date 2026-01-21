from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    '''
    Represents the Login form, used to inject CSS ID's and to ensure
    fields repopulation when realoading the page.
    '''

    username = forms.CharField(
        max_length = 30,
        strip = True,
        label = _('Usuário:'),
        widget = forms.TextInput(attrs={
            'id': 'username',
            'autofocus': True,
            'placeholder': 'Digite seu nome de usuário',
        })
    )

    password = forms.CharField(
        label = _('Senha:'),
        widget = forms.PasswordInput(attrs={
            'id': 'password',
            'placeholder': 'Digite sua senha',
        })
    )