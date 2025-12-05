from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    def __str__(self):
        return self.username


class Client(models.Model):
    '''
    Represents the clients table in the database.

    Columns:
    - id: Unique primary key.
    - name: Client's name.
    - rg: General Registry (RG) of the client.
    - cpf: Individual Taxpayer Registry (CPF) of the client.
    - phone_number: Client's phone number.
    - birth_date: Client's date of birth.
    - created_at: The time the object was instantiated.
    - updated_at: The time the object was updated.
    '''

    name = models.CharField(_('Nome'), max_length=255)
    cpf = models.CharField(_('CPF'), max_length=14, unique=True)

    # Rg is blank=null=True because in 2032 it won't be mandatory anymore
    rg = models.CharField(_('RG'), max_length=20, blank=True, null=True)
    phone_number = models.CharField(_('Telefone'), max_length=20, blank=True)
    birth_date = models.DateField(_('Data de Nascimento'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')


    def __str__(self):
        return f'{self.name} ({self.cpf})'


class Entrance(models.Model):

    class DepartmentChoices(models.TextChoices):
        # department = value, label
        COAG = 'COAG', 'Coordenação de Administração Geral'
        GEAD = 'GEAD', 'Gerência de Administração'
        NUINF = 'NUINF', 'Núcleo de Informática'
        NUMAP = 'NUMAP', 'Núcleo de Material e Patrimônio'
        GEOFIN = 'GEOFIN', 'Gerência de Orçamento e Finanças'
        GEPES = 'GEPES', 'Gerência de Pessoas'
        CODES = 'CODES', 'Coordenação de Desenvolvimento'
        DIDOT = 'DIDOT', 'Diretoria de Desenvolvimento e Territorial'
        GETEDEC = 'GETEDEC', 'Gerência de Gestão do Território e Desevolvimento Econômico'
        DIART = 'DIART', 'Diretoria de Articulação'
        GEPSCEL = 'GEPSCEL', 'Gerência de Políticas Sociais, Cultura, Esporte e Lazer'
        COLOM = 'COLOM', 'Coordenação de Licenciamento, Obras e Manutenção'
        DIALIC = 'DIALIC', 'Diretoria de Aprovação e Licenciamento'
        GELOAE = 'GELOAE', 'Gerência de Licenciamento de Obras e Atividades Econômicas'
        GEAPRO = 'GEAPRO', 'Gerência de Elaboração e Aprovação de Projetos'
        DIROB = 'DIROB', 'Diretoria de Obras'
        GEOB = 'GEOB', 'Gerência de Obras'
        GEMAC = 'GEMAC', 'Gerência de Manutenção e Conservação'
        ASCOM = 'ASCOM', 'Assessoria de comunicação'
        ASTEC = 'ASTEC', 'Assessoria Técnica'
        ASPLAN = 'ASPLAN', 'Assessoria de Planejamento'
        GAB = 'GAB', 'Gabinete'
        OUV = 'OUV', 'Ouvidoria'
        JSM = 'JSM', 'Junta de Serviço Militar'


    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Cliente'))
    created_at = models.DateTimeField(_('Horário de Entrada'), auto_now_add=True)
    department = models.CharField(_('Departamento'), choices=DepartmentChoices.choices)


    class Meta:
        verbose_name = _('Entrada')
        verbose_name_plural = _('Entradas')

    def __str__(self):
        return f'Entrada de {self.client.name} em {self.created_at}'