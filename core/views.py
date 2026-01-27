from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import ListView, View, FormView
from .models import Entrance, Client
from .forms import ClientEntryForm, SearchClientForm
from django.utils import timezone
import json
from django.db import transaction
from django.urls import reverse_lazy
import re
from validate_docbr import CPF
from .formatters import format_phone_number, format_cpf


class EntranceSoftDeleteView(LoginRequiredMixin, View):
    '''
    View used to mark the Entrance as cancelled. If it's the 1st
    entrance of a client, it also cancels the client to release the CPF.
    '''

    def post(self, request, pk: int):

        entrance: Entrance = get_object_or_404(Entrance, pk=pk)
        today = timezone.localdate()

        # Checks if the deletion is happening at current date
        if entrance.created_at.date() != today:
            return JsonResponse({
                'type': 'error',
                'message': '''Só é possível excluir entradas na data atual. Contate o administrador do sistema para outros períodos.''',
                'dict': {}
            }, status=403)

        with transaction.atomic():

            # Cancels entrance
            entrance.status = Entrance.Status.CANCELLED
            entrance.save()

            # Cancels client if there's no regular entrances for this client
            client = entrance.client
            has_valid_entrances = Entrance.objects.filter(
                    client=client,
                    status=Entrance.Status.REGULAR
                ).exists()

            if not has_valid_entrances:
                client.status = Client.Status.CANCELLED
                client.save()

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
        return Entrance.objects.select_related('client')\
            .filter(created_at__date=today, status=Entrance.Status.REGULAR)\
            .order_by('-created_at')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_entry_form'] = ClientEntryForm()
        context['search_client_form'] = SearchClientForm()

        return context


class EntranceCreateView(LoginRequiredMixin, FormView):
    '''
    View used to add a new Entrance/Client.
    '''

    template_name = 'core/main/main.html'
    form_class = ClientEntryForm
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


    def form_valid(self, form: ClientEntryForm):

        data = form.cleaned_data

        cpf = data.get('cpf')
        name = data.get('name')
        birth_date = data.get('birth_date')
        phone_number = data.get('phone_number')
        department = data.get('department')

        with transaction.atomic():

            # Searchs for a regular client
            client = Client.objects.filter(
                cpf=cpf,
                status=Client.Status.REGULAR
            ).first()

            # If a regular client already exists, then we only have to
            # update his information. Otherwise, we create a new one.
            if client:
                client.phone_number = phone_number
                client.save()
            else:
                client = Client.objects.create(
                    name=name,
                    cpf=cpf,
                    birth_date=birth_date,
                    phone_number=phone_number
                )

            # Registers entrance
            Entrance.objects.create(
                client=client,
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
    Represents the view used to look for a client
    using his CPF.
    '''

    form_class = SearchClientForm

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
            .select_related('client')
            .filter(
                client__cpf=cpf,
                created_at__date=today,
                status=Entrance.Status.REGULAR,
            )
            .order_by('-created_at')
        )

        if not entrances:
            return JsonResponse({
                'type': 'info',
                'message': 'Cliente não encontrado!',
                'dict': {}
            }, status=404)

        client = entrances[0].client

        entrances_data = []
        for entrance in entrances:

            local_dt = timezone.localtime(entrance.created_at)

            entrances_data.append({
                'id': entrance.id,
                'department': entrance.department,
                'entrance_date': local_dt.strftime('%d/%m/%Y'),
                'entrance_time': local_dt.strftime('%H:%M:%S'),
            })

        return JsonResponse({
            'type': 'success',
            'message': 'Cliente encontrado!',
            'dict': {
                'client': {
                'name': client.name,
                'cpf': format_cpf(client.cpf),
                'phone_number': format_phone_number(client.phone_number),
                'birth_date': client.birth_date.strftime('%d/%m/%Y'),
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


class ClientDetailView(LoginRequiredMixin, View):
    '''
    View dedicated to fetching client data for auto-filling
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


        # Trying to find the client
        client = Client.objects.filter(
            cpf=cpf,
            status=Client.Status.REGULAR
        ).first()


        # If client is not registered yet
        if not client:
            return JsonResponse({
                'type': 'info',
                'message': 'Cliente não encontrado, favor seguir com o cadastro.',
                'dict': {}
            }, status=404)


        return JsonResponse({
            'type': 'success',
            'message': 'Cliente encontrado!',
            'dict': {
                'name': client.name,
                'birth_date': client.birth_date.strftime('%d/%m/%Y'),
                'phone_number': format_phone_number(client.phone_number),
                'status': client.status,
            }
        }, status=200)