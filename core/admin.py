from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Entrance, User, Department
from import_export.admin import ImportExportModelAdmin


# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'acronym')
    search_fields = ('name', 'acronym')


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'cpf', 'phone_number', 'birth_date', 'created_at', 'status')
    search_fields = ('name', 'cpf', 'phone_number')
    list_filter = ('created_at', 'status')
    readonly_fields = ('id', 'created_at', 'updated_at')

    ordering = ('-created_at',)


@admin.register(Entrance)
class EntranceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'client', 'department', 'created_at', 'status')
    search_fields = ('client__cpf', 'client__name')
    list_filter = ('department', 'status', 'created_at')
    readonly_fields = ('id', 'created_at')

    autocomplete_fields = ('client',)

    def get_readonly_fields(self, request, obj=None):

        base_readonly = super().get_readonly_fields(request, obj)

        if obj:
            return base_readonly + ('client', 'department')
        return base_readonly