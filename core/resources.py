from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Citizen, Department, Entrance

class EntranceResource(resources.ModelResource):
    citizen = fields.Field(
        column_name='CPF',
        attribute='citizen',
        widget=ForeignKeyWidget(Citizen, field='cpf')
    )

    department = fields.Field(
        column_name='Departamento',
        attribute='department',
        widget=ForeignKeyWidget(Department, field='acronym')
    )

    created_at = fields.Field(attribute='created_at', column_name='Data de Criação')

    class Meta:
        model = Entrance
        fields = ('id', 'citizen', 'department', 'created_at', 'status')
        export_order = fields


    def dehydrate_status(self, obj):
        return obj.get_status_display()


class DepartmentResource(resources.ModelResource):

    name = fields.Field(attribute='name', column_name='Nome')
    acronym = fields.Field(attribute='acronym', column_name='Sigla')

    class Meta:
        model = Citizen
        fields = (
            'id',
            'name',
            'acronym',
            'is_available',
        )
        export_order = fields


class CitizenResource(resources.ModelResource):

    name = fields.Field(attribute='name', column_name='Nome')
    cpf = fields.Field(attribute='cpf', column_name='CPF')
    phone_number = fields.Field(attribute='phone_number', column_name='Telefone')
    birth_date = fields.Field(attribute='birth_date', column_name='Data de Nascimento')
    created_at = fields.Field(attribute='created_at', column_name='Data de Criação')

    class Meta:
        model = Citizen
        fields = (
            'id',
            'name',
            'cpf',
            'phone_number',
            'birth_date',
            'created_at',
            'status',
        )
        export_order = fields

    def dehydrate_status(self, obj):
        return obj.get_status_display()


