import pytest
from django.urls import reverse
from model_bakery import baker
from core.models import Entrance, Status
from django.utils import timezone

@pytest.mark.django_db
class TestEntranceListView:

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