from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    '''Represents the User's table in the database.'''


    class Meta:
        verbose_name= 'Usuário'
        verbose_name_plural= 'Usuários'


    def __str__(self):
        return self.username


class Client(models.Model):
    '''
    Represents the Client's table in the database.

    Columns:
    - id: Unique primary key.
    - name: Client's name.
    - cpf: Individual Taxpayer Registry (CPF) of the client.
    - birth_date: Client's date of birth.
    - created_at: The time the object was instantiated.
    - updated_at: The time the object was updated.
    '''


    class Status(models.TextChoices):
        REGULAR = 'REGULAR', _('Regular')
        CANCELLED = 'CANCELLED', _('Cancelado')


    name = models.CharField(_('Nome'), max_length=255)
    cpf = models.CharField(_('CPF'), max_length=11)
    birth_date = models.DateField(_('Data de Nascimento'), blank=False)
    phone_number = models.CharField(_('Telefone'), max_length=20, blank=True)

    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.REGULAR,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

        constraints = [
            models.UniqueConstraint(
                fields=['cpf'],
                condition=models.Q(status='REGULAR'),
                name='unique_active_cpf'
            )
        ]


    def __str__(self):
        return f'{self.name} ({self.cpf})'


class Department(models.Model):
    name = models.CharField(_('Nome'), max_length=100)
    acronym = models.CharField(_('Sigla'), max_length=10)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['name']

    def __str__(self):
        return f"{self.acronym}"


class Entrance(models.Model):

    '''
    Represents the Entrance's table in the database.

    Columns:
    - id: Unique primary key.
    - client (FK): Reference to the client who visited a certain department.
    '''


    class Status(models.TextChoices):
        REGULAR = 'REGULAR', _('Regular')
        CANCELLED = 'CANCELLED', _('Cancelado')


    client = models.ForeignKey(
        Client,
        related_name='entrances',
        on_delete=models.CASCADE,
        verbose_name=_('Cliente')
    )

    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.REGULAR,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name='Departamento',
        related_name='entrances'
    )

    created_at = models.DateTimeField(_('Horário de Entrada'), auto_now_add=True)


    class Meta:
        verbose_name = _('Entrada')
        verbose_name_plural = _('Entradas')


    def __str__(self):
        return f'Entrada de {self.client.name} em {self.created_at}'