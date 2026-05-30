import pytest
from django.urls import reverse
from model_bakery import baker
from core.models import Status, Citizen, Entrance
from django.utils import timezone
import json
from datetime import date


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

    def test_with_valid_query(self, logged_in_client):
        """
        Testing for when a client exists, the payload is valid and the CPF is valid.
        It should return a JSON response with status 200 and the client's information.
        """

        baker.make(
            "core.Citizen",
            name="John Doe Smith",
            cpf="13610361093",
            birth_date="1985-12-25",
            phone_number="61912345678",
            status=Status.REGULAR,
        )

        json_response = logged_in_client.post(
            self.URL,
            data=json.dumps({"cpf": "136.103.610-93"}),
            content_type="application/json",
        )

        response_content = json_response.json()

        assert json_response.status_code == 200, json_response
        assert response_content["type"] == "success"
        assert response_content["dict"]["name"] == "John Doe Smith"
        assert response_content["dict"]["birth_date"] == "25/12/1985"
        assert response_content["dict"]["phone_number"] == "(61) 91234-5678"

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
        Testing for when the client exists, the CPF is valid, but the payload is invalid.
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

    def test_delete_entrance_today_with_other_valid_entrances(self, logged_in_client):
        """
        Date is today (True) + Citizen has other entrances (True).
        The target entrance is cancelled, but the citizen MUST remain REGULAR.
        """

        citizen = baker.make("core.Citizen", status=Status.REGULAR)

        target_entrance = baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=timezone.now(),
        )

        # Another existing valid entrance
        baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=timezone.now(),
        )

        response = logged_in_client.post(self.get_url(target_entrance.pk))

        target_entrance.refresh_from_db()
        citizen.refresh_from_db()

        assert response.status_code == 200
        assert target_entrance.status == Status.CANCELLED
        assert citizen.status == Status.REGULAR

    def test_delete_entrance_today_with_no_other_valid_entrances(
        self, logged_in_client
    ):
        """
        Date is today (True) + Citizen has NO other entrances (False).
        The target entrance is cancelled AND the citizen MUST be cancelled.
        """

        citizen = baker.make("core.Citizen", status=Status.REGULAR)

        target_entrance = baker.make(
            "core.Entrance",
            citizen=citizen,
            status=Status.REGULAR,
            created_at=timezone.now(),
        )

        response = logged_in_client.post(self.get_url(target_entrance.pk))

        target_entrance.refresh_from_db()
        citizen.refresh_from_db()

        assert response.status_code == 200
        assert target_entrance.status == Status.CANCELLED
        assert citizen.status == Status.CANCELLED


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

    def test_create_entrance_for_existing_citizen_updates_phone(self, logged_in_client):
        """
        Testing for when the citizen already exists. The system must not duplicate
        the citizen, but update their phone number and create a new entrance.
        """

        existing_citizen = baker.make(
            "core.Citizen",
            name="Jane Doe",
            birth_date=date(1990, 5, 15),
            cpf="13610361093",
            phone_number="61 888888888",
            status=Status.REGULAR,
        )
        department = baker.make("core.Department", is_available=True)

        payload = {
            "cpf": "136.103.610-93",
            "name": existing_citizen.name,
            "birth_date": existing_citizen.birth_date.strftime("%d/%m/%Y"),
            "phone_number": "(61) 91111-2222",
            "department": department.pk,
        }

        response = logged_in_client.post(
            self.URL, data=json.dumps(payload), content_type="application/json"
        )

        existing_citizen.refresh_from_db()

        assert response.status_code == 200
        assert Citizen.objects.count() == 1
        assert existing_citizen.phone_number != "61 888888888"
        assert Entrance.objects.filter(
            citizen=existing_citizen, department=department
        ).exists()

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

        citizen = baker.make("core.Citizen", cpf="13610361093", status=Status.REGULAR)
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

        citizen = baker.make("core.Citizen", cpf="13610361093", status=Status.REGULAR)

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
