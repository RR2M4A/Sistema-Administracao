from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Client(models.Model):
    """
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
    """

    name = models.CharField("Nome", max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    rg = models.CharField("RG", max_length=20, blank=True, null=True)
    phone_number = models.CharField("Telefone", max_length=20)
    birth_date = models.DateField("Data de Nascimento", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        pass

    def __str__(self):
        return f"{self.name} ({self.cpf})"


class Entrance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Horário de Entrada", auto_now_add=True)


    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return f"Entrada de {self.client.name} em {self.created_at}"