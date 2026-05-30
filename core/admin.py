from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Citizen, Entrance, User, Department
from import_export.admin import ExportActionModelAdmin
from rangefilter.filters import DateRangeFilterBuilder
from .resources import EntranceResource, CitizenResource, DepartmentResource
from simple_history.admin import SimpleHistoryAdmin
import re


# Register your models here.
admin.site.register(User, UserAdmin)


@admin.register(Department)
class DepartmentAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    resource_class = DepartmentResource

    list_display = ("name", "acronym", "is_available")
    search_fields = ("name", "acronym")


@admin.register(Citizen)
class CitizenAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    resource_class = CitizenResource

    list_display = (
        "id",
        "name",
        "cpf",
        "phone_number",
        "birth_date",
        "created_at",
    )
    search_fields = ("name", "cpf", "phone_number")
    list_filter = (("created_at", DateRangeFilterBuilder(title="Data de Criação")),)
    readonly_fields = ("id", "created_at", "updated_at")

    ordering = ("-created_at",)


@admin.register(Entrance)
class EntranceAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    resource_class = EntranceResource

    list_display = ("id", "citizen", "department", "created_at", "status")
    search_fields = ()
    list_filter = (
        ("created_at", DateRangeFilterBuilder(title="Data de Criação")),
        "department",
        "status",
    )
    readonly_fields = ("id", "created_at")

    autocomplete_fields = ("citizen",)

    def get_search_results(self, request, queryset, search_term):
        search_term = search_term.strip()
        possible_cpf = re.sub(r"[\-\.]", "", search_term)

        if possible_cpf.isdigit() and len(possible_cpf) == 11:
            queryset = queryset.filter(citizen__cpf=possible_cpf)
        else:
            queryset = queryset.filter(citizen__name__icontains=search_term)

        return queryset, False

    # Optimization
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("citizen", "department")

    # Makes readonly_objects not editable
    def get_readonly_fields(self, request, obj=None):

        base_readonly = super().get_readonly_fields(request, obj)

        if obj:
            return base_readonly + ("citizen", "department")
        return base_readonly
