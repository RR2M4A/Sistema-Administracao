from datetime import date
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Client, Entrance
from .regex_patterns import RegexPatterns
from validate_docbr import CPF
import re


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


class ClientEntryForm(forms.ModelForm):
    '''
    Represents the Client Entry Form, used to register a client when
    he arrives at the reception.
    '''

    class Meta:
        model = Client
        fields = ['name', 'cpf', 'birth_date', 'phone_number']

        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'add-name',
                'autofocus': True,
                'placeholder': 'Digite o nome completo',
            }),
            'cpf': forms.TextInput(attrs={
                'id': 'add-cpf',
                'placeholder': '000.000.000-00',
            }),
            'birth_date': forms.DateInput(attrs={
                'id': 'add-birth-date',
                'placeholder': 'dd/mm/aaaa',
                'type': 'date'
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'add-phone-number',
                'placeholder': '(00) 00000-0000',
            }),
        }

        labels = {
            'name': _('Nome'),
            'cpf': _('CPF'),
            'birth_date': _('Data de Nascimento'),
            'phone_number': _('Telefone'),
        }


    department = forms.ChoiceField(
        label = _('Departamento'),
        choices = Entrance.DepartmentChoices.choices,
        widget=forms.Select(attrs={
            'id': 'add-department',
        })
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].choices = [('', 'Selecione um departamento')] + list(self.fields['department'].choices)


    def clean_phone_number(self):
        '''Checks if the phone number is valid.'''

        data = self.cleaned_data.get('phone_number', '')
        pattern = RegexPatterns.PHONE_NUMBER.value

        if not data: return data

        if not re.fullmatch(pattern, data):
            raise ValidationError(
                _('Número de telefone inválido!')
            )

        return data


    def clean_cpf(self):
        '''Checks if the CPF is valid and removes punctuation.'''

        data = self.cleaned_data.get('cpf', '')
        validator = CPF()

        data = re.sub(r'\D', '', data)

        if not validator.validate(data):
            raise ValidationError(_('CPF Inválido! Verifique os dígitos.'))

        return data


    def clean_birth_date(self):
        '''Checks if the birth_date is valid. '''

        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()

        if not birth_date: return birth_date

        if birth_date > today:
            raise ValidationError(_('A data de nascimento não pode estar no futuro.'))

        return birth_date


class SearchClientForm(forms.Form):
    '''
    Represents the Search Client Form, used to look for a client
    by his CPF.
    '''

    cpf = forms.CharField(
        label='CPF',
        required=False,
        max_length=14,
        widget=forms.TextInput(attrs={
            'id': 'search-bar',
            'class': 'search-bar',
            'placeholder': 'Digite o CPF aqui',
        })
    )

    def clean_cpf(self):
        '''Removes punctuation from CPF.'''

        data = self.cleaned_data.get('cpf', '')
        data = re.sub(r'\D', '', data)

        return data