import pytest
from django.urls import reverse
from model_bakery import baker
from core.models import Entrance, Status
from django.utils import timezone
import json

@pytest.mark.django_db
class TestEntranceListView:
    """
    Class responsible for holding the 'EntranceListView' tests.
    """

    URL = reverse('core:main')

    def test_access_without_authenticated_user(self, client):
        """
        Testing to access the view without an authenticated user.
        It should return an HTML page with status 302.
        """

        response = client.get(self.URL)
        assert response.status_code == 302


    def test_access_with_authenticated_user_and_valid_entrances(self, logged_in_client):
        """
        Testing to access the view with an authenticated user and valid entrances.
        It should return an HTML page with status 200, and all the valid entrances.
        """

        entrances = baker.make(
            'core.Entrance',
            status=Status.REGULAR,
            created_at=timezone.now(),
            _quantity=10
        )

        response = logged_in_client.get(self.URL)

        assert response.status_code == 200
        for entrance in entrances:
            assert entrance in response.context['entrances']


    def test_access_with_authenticated_user_but_cancelled_entrances(self, logged_in_client):
        """
        Testing to access the view with an authenticated user, but CANCELLED entrances.
        It should return an HTML page with status 200, but no entrances at all.
        """

        entrances = baker.make(
            'core.Entrance',
            status=Status.CANCELLED,
            created_at=timezone.now(),
            _quantity=10
        )

        response = logged_in_client.get(self.URL)

        assert response.status_code == 200
        for entrance in entrances:
            assert entrance not in response.context['entrances']


    def test_access_with_authenticated_user_but_not_today_date(self, logged_in_client):
        """
        Testing to access the view with an authenticated user, but dates different of today.
        It should return an HTML page with status 200, but no entrances at all.
        """

        entrances = baker.make(
            'core.Entrance',
            status=Status.REGULAR,
            created_at=timezone.now() - timezone.timedelta(days=1),
            _quantity=10
        )

        response = logged_in_client.get(self.URL)

        assert response.status_code == 200
        for entrance in entrances:
            assert entrance not in response.context['entrances']


class TestCitizenDetailView:
    """
    Class responsible for holding the 'CitizenDetailView' tests.
    """

    URL = reverse('core:client-detail')

    def test_access_without_authenticated_user(self, client):
        """
        Testing to access the view without an authenticated user.
        It should return an HTML page with status 302.
        """

        response = client.get(self.URL)
        assert response.status_code == 302


    def test_with_valid_query(self, logged_in_client):
        """
        Testing for when a client exists, the payload is valid and the CPF is valid.
        It should return a JSON response with status 200 and the client's information.
        """

        target_citizen = baker.make(
            'core.Citizen',
            name="John Doe Smith",
            cpf="13610361093",
            birth_date="1985-12-25",
            phone_number="61912345678",
            status=Status.REGULAR
        )
        
        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({'cpf': '136.103.610-93'}),
            content_type='application/json'
        )

        response_content = json_response.json()

        assert json_response.status_code == 200, json_response
        assert response_content['type'] == 'success'
        assert response_content['dict']['name'] == "John Doe Smith"
        assert response_content['dict']['birth_date'] == "25/12/1985"
        assert response_content['dict']['phone_number'] == "(61) 91234-5678"


    def test_without_an_existing_client(self, logged_in_client):
        """
        Testing for when the payload is valid, the CPF is valid, but the client doesn't exist.
        It should return a JSON response with status 404.
        """
        
        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({'cpf': '136.103.610-93'}),
            content_type='application/json'
        )

        assert json_response.status_code == 404


    def test_with_an_invalid_cpf(self, logged_in_client):
        """
        Testing for when the payload is valid, the client exists, but the CPF is invalid.
        It should return a JSON response with status 400.
        """
        
        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({'cpf': '000.000.000-00'}),
            content_type='application/json'
        )

        assert json_response.status_code == 400


    def test_with_an_invalid_payload(self, logged_in_client):
        """
        Testing for when the client exists, the CPF is valid, but the payload is invalid.
        It should return a JSON response with status 400.
        """
        
        json_response = logged_in_client.post(
            self.URL,
            data="not_a_json_format",
            content_type='application/json'
        )

        assert json_response.status_code == 400