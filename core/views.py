from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, View, FormView
from .models import Entrance, Citizen, Status
from .forms import CitizenEntryForm, SearchCitizenForm
from django.utils import timezone
import json
from django.db import transaction
from django.urls import reverse_lazy
import re
from validate_docbr import CPF
from .utils.formatters import format_phone_number, format_cpf


class EntranceSoftDeleteView(LoginRequiredMixin, View):
    '''
    View used to mark the Entrance as cancelled. If it's the 1st
    entrance of a citizen, it also cancels the citizen to release the CPF.
    '''

    def post(self, request, pk: int):

        entrance: Entrance = get_object_or_404(Entrance, pk=pk)
        entrance_local = timezone.localtime(entrance.created_at)
        today = timezone.localdate()
        print(entrance_local)

        # Checks if the deletion is happening at current date
        if entrance_local.date() != today:
            return JsonResponse({
                'type': 'error',
                'message': '''Só é possível excluir entradas na data atual. Contate o administrador do sistema para outros períodos.''',
                'dict': {}
            }, status=403)

        with transaction.atomic():

            # Cancels entrance
            entrance.status = Status.CANCELLED
            entrance.save()

            # Cancels citizen if there's no regular entrances for this citizen
            citizen = entrance.citizen
            has_valid_entrances = Entrance.objects.filter(
                    citizen=citizen,
                    status=Status.REGULAR
                ).exists()

            if not has_valid_entrances:
                citizen.status = Status.CANCELLED
                citizen.save()

        return JsonResponse({
            'type': 'success',
            'message': '''Entrada removida com sucesso!''',
            'dict': {}
        }, status=200)


class EntranceListView(LoginRequiredMixin, ListView):
    '''
    Represents the main view, used to display
    the entrances table and the register form.
    '''

    template_name = 'core/main/main.html'
    context_object_name = 'entrances'
    paginate_by = 25

    def get_queryset(self):
        today = timezone.localdate()
        return Entrance.objects.select_related('citizen')\
            .filter(created_at__date=today, status=Status.REGULAR)\
            .order_by('-created_at')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citizen_entry_form'] = CitizenEntryForm()
        context['search_citizen_form'] = SearchCitizenForm()

        return context


class EntranceCreateView(LoginRequiredMixin, FormView):
    '''
    View used to add a new Entrance/Citizen.
    '''

    template_name = 'core/main/main.html'
    form_class = CitizenEntryForm
    success_url = reverse_lazy('core:main')


    # Used to read JSON form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.content_type == 'application/json':
            try:
                data = json.loads(self.request.body)
                kwargs['data'] = data
            except json.JSONDecodeError:
                kwargs['data'] = {}

        return kwargs


    def form_valid(self, form: CitizenEntryForm):

        data = form.cleaned_data

        cpf = data.get('cpf')
        name = data.get('name')
        birth_date = data.get('birth_date')
        phone_number = data.get('phone_number')
        department = data.get('department')

        with transaction.atomic():

            # Searchs for a regular citizen
            citizen = Citizen.objects.filter(
                cpf=cpf,
                status=Status.REGULAR
            ).first()

            # If a regular citizen already exists, then we only have to
            # update his information. Otherwise, we create a new one.
            if citizen:
                citizen.phone_number = phone_number
                citizen.save()
            else:
                citizen = Citizen.objects.create(
                    name=name,
                    cpf=cpf,
                    birth_date=birth_date,
                    phone_number=phone_number
                )

            # Registers entrance
            Entrance.objects.create(
                citizen=citizen,
                department=department
            )

        return JsonResponse({
            'type': 'success',
            'message': 'Entrada registrada com sucesso!',
            'dict': {}
        }, status=200)


    def form_invalid(self, form):
        return JsonResponse({
            'type': 'error',
            'message': 'Verifique os dados informados.',
            'dict': form.errors
        }, status=400)


class EntrancesByCPFView(LoginRequiredMixin, FormView):
    '''
    Represents the view used to look for a citizen
    using his CPF.
    '''

    form_class = SearchCitizenForm

    # Used to read JSON form
    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        if self.request.content_type == 'application/json':
            try:
                data = json.loads(self.request.body)
                kwargs['data'] = data
            except json.JSONDecodeError:
                kwargs['data'] = {}

        return kwargs


    def form_valid(self, form):

        cpf = form.cleaned_data['cpf']
        today = timezone.localdate()

        entrances = (
            Entrance.objects
            .select_related('citizen')
            .filter(
                citizen__cpf=cpf,
                created_at__date=today,
                status=Status.REGULAR,
            )
            .order_by('-created_at')
        )

        if not entrances.exists():
            return JsonResponse({
                'type': 'info',
                'message': 'Cidadão não encontrado!',
                'dict': {}
            }, status=404)

        citizen = entrances[0].citizen

        entrances_data = []
        for entrance in entrances:

            local_dt = timezone.localtime(entrance.created_at)

            entrances_data.append({
                'id': entrance.id,
                'department': entrance.department.acronym,
                'entrance_date': local_dt.strftime('%d/%m/%Y'),
                'entrance_time': local_dt.strftime('%H:%M:%S'),
            })

        return JsonResponse({
            'type': 'success',
            'message': 'Cidadão encontrado!',
            'dict': {
                'citizen': {
                'name': citizen.name,
                'cpf': format_cpf(citizen.cpf),
                'phone_number': format_phone_number(citizen.phone_number),
                'birth_date': citizen.birth_date.strftime('%d/%m/%Y'),
            },

            'entrances': entrances_data
            }
        }, status=200)


    def form_invalid(self, form):
        return JsonResponse({
            'status': 'error',
            'message': 'Dados inválidos.',
            'data': form.errors
        }, status=400)


class CitizenDetailView(LoginRequiredMixin, View):
    '''
    View dedicated to fetching citizen data for auto-filling
    the registration form.
    '''

    def post(self, request):

        # Checks whether the request sent a JSON or not, since
        # this view is made for assyncronous communication.
        try:
            data = json.loads(request.body)
            cpf = data.get('cpf', '')

        except json.JSONDecodeError:
            return JsonResponse({
                'type': 'error',
                'message': 'JSON Inválido!',
                'dict': {}
            }, status=400)


        cpf = re.sub(r'\D', '', cpf)
        validator = CPF()

        # Checks if CPF is valid to give a fast feedback to frontend
        if not validator.validate(cpf):
            return JsonResponse({
                'type': 'warning',
                'message': 'CPF Inválido! Verifique os dígitos.',
                'dict': {}
            }, status=400)


        # Trying to find the citizen
        citizen = Citizen.objects.filter(
            cpf=cpf,
            status=Status.REGULAR
        ).first()


        # If citizen is not registered yet
        if not citizen:
            return JsonResponse({
                'type': 'info',
                'message': 'Cidadão não encontrado, favor seguir com o cadastro.',
                'dict': {}
            }, status=404)


        return JsonResponse({
            'type': 'success',
            'message': 'Cidadão encontrado!',
            'dict': {
                'name': citizen.name,
                'birth_date': citizen.birth_date.strftime('%d/%m/%Y'),
                'phone_number': format_phone_number(citizen.phone_number),
                'status': citizen.status,
            }
        }, status=200)
