import json
from datetime import date
import pytest
from django.urls import reverse
from django.utils import timezone

from model_bakery import baker

from core.models import Status, Citizen, Entrance


@pytest.mark.django_db
class TestEntranceListView:
    """
    Class responsible for holding the 'EntranceListView' tests.
    """

    URL = reverse("core:main")

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
            "core.Entrance",
            status=Status.REGULAR,
            created_at=timezone.now(),
            _quantity=10,
        )

        response = logged_in_client.get(self.URL)

        assert response.status_code == 200
        for entrance in entrances:
            assert entrance in response.context["entrances"]

    def test_access_with_authenticated_user_but_cancelled_entrances(
        self, logged_in_client
    ):
        """
        Testing to access the view with an authenticated user, but CANCELLED entrances.
        It should return an HTML page with status 200, but no entrances at all.
        """

        entrances = baker.make(
            "core.Entrance",
            status=Status.CANCELLED,
            created_at=timezone.now(),
            _quantity=10,
        )

        response = logged_in_client.get(self.URL)

        assert response.status_code == 200
        for entrance in entrances:
            assert entrance not in response.context["entrances"]

    def test_access_with_authenticated_user_but_not_today_date(self, logged_in_client):
        """
        Testing to access the view with an authenticated user, but dates different of today.
        It should return an HTML page with status 200, but no entrances at all.
        """

        entrances = baker.make(
            "core.Entrance",
            status=Status.REGULAR,
            created_at=timezone.now() - timezone.timedelta(days=1),
            _quantity=10,
        )

        response = logged_in_client.get(self.URL)

        assert response.status_code == 200
        for entrance in entrances:
            assert entrance not in response.context["entrances"]


@pytest.mark.django_db
class TestCitizenDetailView:
    """
    Class responsible for holding the 'CitizenDetailView' tests.
    """

    URL = reverse("core:client-detail")

    def test_access_without_authenticated_user(self, client):
        """
        Testing to access the view without an authenticated user.
        It should return an HTML page with status 302.
        """

        response = client.get(self.URL)
        assert response.status_code == 302

    def test_with_valid_query_created_today_can_edit(self, logged_in_client):
        """
        Testing a valid query for a citizen created TODAY.
        It should return the client's information and 'can_edit' as True.
        """

        baker.make(
            "core.Citizen",
            name="John Doe Smith",
            cpf="13610361093",
            birth_date=date(1985, 12, 25),
            phone_number="61912345678",
            created_at=timezone.now(),
        )

        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "136.103.610-93"}),
            content_type="application/json",
        )

        response_content = json_response.json()

        assert json_response.status_code == 200
        assert response_content["type"] == "success"
        assert response_content["dict"]["name"] == "John Doe Smith"
        assert (
            response_content["dict"]["can_edit"] is True
        )  # Validation of Grace Period

    def test_with_valid_query_created_past_cannot_edit(self, logged_in_client):
        """
        Testing a valid query for a citizen created in the PAST.
        It should return the client's information and 'can_edit' as False.
        """

        past_date = timezone.now() - timezone.timedelta(days=5)

        baker.make(
            "core.Citizen",
            name="John Doe",
            cpf="13610361093",
            created_at=past_date,
        )

        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "136.103.610-93"}),
            content_type="application/json",
        )

        response_content = json_response.json()
        assert json_response.status_code == 200
        assert response_content["dict"]["can_edit"] is False

    def test_without_an_existing_client(self, logged_in_client):
        """
        Testing for when the payload is valid, the CPF is valid, but the client doesn't exist.
        It should return a JSON response with status 404.
        """

        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "136.103.610-93"}),
            content_type="application/json",
        )

        assert json_response.status_code == 404

    def test_with_an_invalid_cpf(self, logged_in_client):
        """
        Testing for when the payload is valid, the client exists, but the CPF is invalid.
        It should return a JSON response with status 400.
        """

        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "000.000.000-00"}),
            content_type="application/json",
        )

        assert json_response.status_code == 400

    def test_with_an_invalid_payload(self, logged_in_client):
        """
        Testing for when the payload is invalid (not JSON).
        It should return a JSON response with status 400.
        """

        json_response = logged_in_client.post(
            self.URL, data="not_a_json_format", content_type="application/json"
        )

        assert json_response.status_code == 400


@pytest.mark.django_db
class TestEntranceSoftDeleteView:
    """
    Class responsible for holding the 'EntranceSoftDeleteView' tests.
    """

    def get_url(self, pk: int) -> str:
        """Helper method to dynamically generate the delete URL."""
        return reverse("core:entrance-cancellation", kwargs={"pk": pk})

    def test_delete_entrance_from_different_date(self, logged_in_client):
        """
        Attempt to delete an entrance from a previous date.
        The system must return a 403 Forbidden status and prevent deletion.
        """

        past_date = timezone.now() - timezone.timedelta(days=1)
        entrance = baker.make(
            "core.Entrance", status=Status.REGULAR, created_at=past_date
        )

        response = logged_in_client.post(self.get_url(entrance.pk))
        entrance.refresh_from_db()

        assert response.status_code == 403
        assert response.json()["type"] == "error"
        assert entrance.status == Status.REGULAR

    def test_hard_delete_if_is_first_entrance(self, logged_in_client):
        """
        If it's the citizen's ONLY entrance, deleting it should trigger a
        hard delete of both the Entrance and the Citizen.
        """

        citizen = baker.make("core.Citizen")
        target_entrance = baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=timezone.now(),
        )

        response = logged_in_client.post(self.get_url(target_entrance.pk))
        assert response.status_code == 200

        # Assert records were physically removed from the DB
        assert not Entrance.objects.filter(pk=target_entrance.pk).exists()
        assert not Citizen.objects.filter(pk=citizen.pk).exists()

    def test_soft_delete_if_citizen_has_multiple_entrances(self, logged_in_client):
        """
        If the citizen has > 1 entrances, deleting the current one should
        only CANCEL the entrance, preserving the citizen and historical entrances.
        """

        citizen = baker.make("core.Citizen")

        # Historical entrance
        baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=timezone.now() - timezone.timedelta(days=30),
        )

        # Today's entrance (target)
        target_entrance = baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=timezone.now(),
        )

        response = logged_in_client.post(self.get_url(target_entrance.pk))

        target_entrance.refresh_from_db()

        assert response.status_code == 200
        assert target_entrance.status == Status.CANCELLED
        assert Citizen.objects.filter(pk=citizen.pk).exists()


@pytest.mark.django_db
class TestEntranceCreateView:
    """
    Class responsible for holding the 'EntranceCreateView' tests.
    """

    URL = reverse("core:add")

    def test_create_new_citizen_and_entrance(self, logged_in_client):
        """
        Testing for when the citizen does not exist.
        The system must create both the Citizen and the Entrance.
        """

        department = baker.make("core.Department", is_available=True)

        payload = {
            "cpf": "136.103.610-93",
            "name": "John Doe",
            "birth_date": "01/01/1990",
            "phone_number": "(61) 99999-9999",
            "department": department.pk,
        }

        response = logged_in_client.post(
            self.URL, data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        assert Citizen.objects.filter(cpf="13610361093").count() == 1
        assert Entrance.objects.count() == 1

    def test_update_citizen_if_created_today_grace_period(self, logged_in_client):
        """
        If the citizen was created TODAY, the system must update phone, name, and birth date.
        """

        existing_citizen = baker.make(
            "core.Citizen",
            name="Jane Doe",
            birth_date=date(1990, 5, 15),
            cpf="13610361093",
            phone_number="61 888888888",
            created_at=timezone.now(),  # Created today
        )
        department = baker.make("core.Department", is_available=True)

        payload = {
            "cpf": "136.103.610-93",
            "name": "Jane Corrected",
            "birth_date": "16/05/1990",
            "phone_number": "(61) 91111-2222",
            "department": department.pk,
        }

        response = logged_in_client.post(
            self.URL, data=json.dumps(payload), content_type="application/json"
        )

        existing_citizen.refresh_from_db()

        assert response.status_code == 200
        assert Citizen.objects.count() == 1

        # Asserts ALL fields were updated
        assert existing_citizen.name == "Jane Corrected"
        assert existing_citizen.birth_date == date(1990, 5, 16)
        assert existing_citizen.phone_number != "61 888888888"

    def test_update_only_phone_if_created_past_grace_period_expired(
        self, logged_in_client
    ):
        """
        If the citizen was created in the PAST, the system must ONLY update the phone number,
        ignoring name and birth date changes.
        """

        past_date = timezone.now() - timezone.timedelta(days=10)
        existing_citizen = baker.make(
            "core.Citizen",
            name="Jane Original",
            birth_date=date(1990, 5, 15),
            cpf="13610361093",
            phone_number="61 888888888",
            created_at=past_date,  # Created in the past
        )
        department = baker.make("core.Department", is_available=True)

        payload = {
            "cpf": "136.103.610-93",
            "name": "Hacker Trying to Change Name",
            "birth_date": "01/01/2000",
            "phone_number": "(61) 91111-2222",  # New phone
            "department": department.pk,
        }

        response = logged_in_client.post(
            self.URL, data=json.dumps(payload), content_type="application/json"
        )

        existing_citizen.refresh_from_db()

        assert response.status_code == 200
        assert Citizen.objects.count() == 1
        assert existing_citizen.phone_number != "61 888888888"

        # Name and Date are NOT updated (Period to edit expired)
        assert existing_citizen.name == "Jane Original"
        assert existing_citizen.birth_date == date(1990, 5, 15)

    def test_invalid_payload_returns_bad_request(self, logged_in_client):
        """
        Testing with invalid payload (missing mandatory birth_date).
        The system must return a 400 Bad Request status.
        """
        department = baker.make("core.Department", is_available=True)

        payload = {
            "cpf": "136.103.610-93",
            "name": "John Doe",
            "department": department.pk,
        }

        response = logged_in_client.post(
            self.URL, data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json()["type"] == "error"
        assert "birth_date" in response.json()["dict"]


@pytest.mark.django_db
class TestEntrancesByCPFView:
    """
    Class responsible for holding the 'EntrancesByCPFView' tests.
    """

    URL = reverse("core:search")

    def test_search_existing_citizen_with_today_entrances(self, logged_in_client):
        """
        Testing for when the citizen exists and has recorded entrances today.
        """

        citizen = baker.make("core.Citizen", cpf="13610361093")
        department = baker.make("core.Department", acronym="GAB")
        baker.make(
            "core.Entrance",
            citizen=citizen,
            department=department,
            status=Status.REGULAR,
            created_at=timezone.now(),
        )

        response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "136.103.610-93"}),
            content_type="application/json",
        )

        response_data = response.json()

        assert response.status_code == 200
        assert response_data["type"] == "success"
        assert len(response_data["dict"]["entrances"]) == 1
        assert response_data["dict"]["entrances"][0]["department"] == "GAB"

    def test_search_citizen_with_no_entrances_today(self, logged_in_client):
        """
        Testing for when the citizen exists but has NO entrances recorded today.
        The system must return a 404 status in the context of today's entrances.
        """
        citizen = baker.make("core.Citizen", cpf="13610361093")

        # Entrance created yesterday
        past_date = timezone.now() - timezone.timedelta(days=1)
        baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=past_date,
        )

        response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "136.103.610-93"}),
            content_type="application/json",
        )

        assert response.status_code == 404
        assert response.json()["type"] == "info"
