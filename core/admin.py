from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client, Entrance, User

# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'phone_number', 'created_at')
    search_fields = ('name', 'cpf', 'rg')
    list_filter = ('created_at',)


@admin.register(Entrance)
class EntranceAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('client__cpf',)