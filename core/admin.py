from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Entrance, User, Department
from import_export.admin import ExportActionModelAdmin
from rangefilter.filters import DateRangeFilterBuilder
from .resources import EntranceResource, ClientResource, DepartmentResource


# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Department)
class DepartmentAdmin(ExportActionModelAdmin):
    resource_class = DepartmentResource

    list_display = ('name', 'acronym')
    search_fields = ('name', 'acronym')


@admin.register(Client)
class ClientAdmin(ExportActionModelAdmin):
    resource_class = ClientResource

    list_display = ('id', 'name', 'cpf', 'phone_number', 'birth_date', 'created_at', 'status')
    search_fields = ('name', 'cpf', 'phone_number')
    list_filter = (
        ('created_at', DateRangeFilterBuilder(title="Data de Criação")),
        'status'
    )
    readonly_fields = ('id', 'created_at', 'updated_at')

    ordering = ('-created_at',)


@admin.register(Entrance)
class EntranceAdmin(ExportActionModelAdmin):
    resource_class = EntranceResource

    list_display = ('id', 'client', 'department', 'created_at', 'status')
    search_fields = ('client__cpf', 'client__name')
    list_filter = (
        ('created_at', DateRangeFilterBuilder(title="Data de Criação")),
        'department',
        'status'
    )
    readonly_fields = ('id', 'created_at')

    autocomplete_fields = ('client',)

    # Optimization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('client', 'department')


    # Makes readonly_objects not editable
    def get_readonly_fields(self, request, obj=None):

        base_readonly = super().get_readonly_fields(request, obj)

        if obj:
            return base_readonly + ('client', 'department')
        return base_readonly