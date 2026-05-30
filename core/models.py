from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords


class Status(models.TextChoices):
    REGULAR = "R", _("Regular")
    CANCELLED = "C", _("Cancelado")


class User(AbstractUser):
    """
    Represents the 'User' table in the database.
    Extends Django's AbstractUser to allow customizations.

    Columns:
    - id: Unique primary key.
    - username: Unique identifier for login.
    - first_name: User's given name.
    - last_name: User's family name.
    - email: User's electronic mail address.
    - password: Hashed password string.
    - is_staff: Boolean indicating if the user can access the admin site.
    - is_active: Boolean indicating if the account is considered active.
    - is_superuser: Boolean granting all permissions without explicitly assigning them.
    - last_login: The last time the user authenticated.
    - date_joined: The time the account was created.
    """

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username


class Citizen(models.Model):
    """
    Represents the 'Citizen' table in the database.

    Columns:
    - id: Unique primary key.
    - name: Citizen's name.
    - cpf: Individual Taxpayer Registry (CPF) of the citizen.
    - birth_date: Citizen's date of birth.
    - created_at: The time the object was instantiated.
    - updated_at: The time the object was updated.
    """

    history = HistoricalRecords()

    name = models.CharField(_("Nome"), max_length=100)
    cpf = models.CharField(
        _("CPF"),
        max_length=11,
        validators=[RegexValidator(r"^\d{11}$", "CPF must have exactly 11 digits")],
        db_index=True,
    )
    birth_date = models.DateField(_("Data de Nascimento"))
    phone_number = models.CharField(_("Telefone"), max_length=20, blank=True)

    status = models.CharField(
        _("Status"),
        max_length=1,
        choices=Status.choices,
        default=Status.REGULAR,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cidadão")
        verbose_name_plural = _("Cidadãos")

        constraints = [
            models.UniqueConstraint(
                fields=["cpf"],
                condition=models.Q(status=Status.REGULAR),
                name="unique_active_cpf",
            )
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_status = Citizen.objects.get(pk=self.pk).status

                # If status has changed from REGULAR to CANCELLED
                if old_status != Status.CANCELLED and self.status == Status.CANCELLED:
                    entrances = self.entrances.filter(status=Status.REGULAR)
                    for entrance in entrances:
                        entrance.status = Status.CANCELLED
                        entrance.save()

            # Saves as usual
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    """
    Represents the 'Department' table in the database.

    Columns:
    - id: Unique primary key.
    - name: Full name of the department (unique).
    - acronym: Short abbreviation of the department (unique).
    - is_available: If the department exists.
    """

    name = models.CharField(_("Nome"), max_length=100, unique=True)
    acronym = models.CharField(_("Sigla"), max_length=10, unique=True)
    is_available = models.BooleanField(_("Disponível"), default=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["name"]

    def __str__(self):
        return f"{self.acronym}"


class Entrance(models.Model):
    """
    Represents the Entrance's table in the database.

    Columns:
    - id: Unique primary key.
    - citizen (FK): Reference to the citizen who visited a certain department.
    """

    history = HistoricalRecords()

    citizen = models.ForeignKey(
        Citizen,
        related_name="entrances",
        on_delete=models.RESTRICT,
        verbose_name=_("Cidadão"),
    )

    status = models.CharField(
        _("Status"),
        max_length=1,
        choices=Status.choices,
        default=Status.REGULAR,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.RESTRICT,
        verbose_name="Departamento",
        related_name="entrances",
    )

    created_at = models.DateTimeField(_("Horário de Entrada"), auto_now_add=True)

    class Meta:
        verbose_name = _("Entrada")
        verbose_name_plural = _("Entradas")

    def __str__(self):
        return f"Entrada de {self.citizen} em {self.created_at}"
