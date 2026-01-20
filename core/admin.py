from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Entrance, User, Phone

# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'birth_date', 'created_at')
    search_fields = ('name', 'cpf')
    list_filter = ('created_at',)


@admin.register(Entrance)
class EntranceAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_at')
    search_fields = ('client__cpf',)
    list_filter = ('created_at',)


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('client', 'number')
    search_fields = ('number', 'client__cpf')