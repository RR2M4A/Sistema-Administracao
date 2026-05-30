import pytest
from faker import Faker
from model_bakery import baker

from ..forms import CitizenEntryForm, SearchCitizenForm


fake = Faker('pt_BR')

def generate_random_data() -> dict:
    """
    Generates random valid data for testing the form.
    Uses date_of_birth to guarantee past dates and prevent flaky tests.
    """
    ddd = fake.random_number(digits=2, fix_len=True)
    number = fake.random_number(digits=8, fix_len=True)

    return {
        'name': fake.name().lower(),
        'cpf': fake.cpf(),
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%d/%m/%Y"),
        'phone_number': f"{ddd} 9{number}",
    }


@pytest.mark.django_db
class TestCitizenEntryForm:
    """
    Class responsible for holding tests of 'CitizenEntryForm'.
    """

    @pytest.mark.parametrize('_', range(5))
    def test_form_is_valid_with_good_data(self, _):
        """
        Testing form when all data is valid.
        It should clean all inputs, capitalize the name, and not throw errors.
        """
        department = baker.make('core.Department', is_available=True)
        data = generate_random_data()
        data['department'] = department.id

        original_name = data['name']

        form = CitizenEntryForm(data=data)

        assert form.is_valid()

        # Verifies if the clean_name() successfully applied .title()
        assert form.cleaned_data['name'] == original_name.title()

    def test_form_is_invalid_with_bad_cpf(self):
        """
        Testing form when the CPF is invalid mathematically,
        but all other data is valid. It should raise a ValidationError on 'cpf'.
        """
        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'John Doe',
            'cpf': '111.111.111-11', # Invalid CPF
            'birth_date': '20/05/1990',
            'phone_number': '61 988887777',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)

        assert not form.is_valid()
        assert 'cpf' in form.errors

    def test_form_is_invalid_with_future_birth_date(self):
        """
        Testing form when the birth date is in the future.
        It should raise a ValidationError on 'birth_date'.
        """
        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'John Doe',
            'cpf': fake.cpf(),
            'birth_date': '20/05/3099',  # Future date
            'phone_number': '61 988887777',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)

        assert not form.is_valid()
        assert 'birth_date' in form.errors

    def test_form_is_invalid_with_bad_birth_date_format(self):
        """
        Testing form when the birth date format is not dd/mm/yyyy.
        It should raise a ValidationError on 'birth_date'.
        """
        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'John Doe',
            'cpf': fake.cpf(),
            'birth_date': '21-11-2001',  # Invalid format (uses dashes)
            'phone_number': '61 988887777',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)

        assert not form.is_valid()
        assert 'birth_date' in form.errors

    def test_form_is_invalid_with_bad_phone_number(self):
        """
        Testing form when the phone number does not match the Regex pattern.
        It should raise a ValidationError on 'phone_number'.
        """
        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'John Doe',
            'cpf': fake.cpf(),
            'birth_date': '20/05/1990',
            'phone_number': '61 123',  # Invalid phone number length
            'department': department.id
        }

        form = CitizenEntryForm(data=data)

        assert not form.is_valid()
        assert 'phone_number' in form.errors

    def test_form_is_invalid_when_missing_required_fields(self):
        """
        Testing form with an empty payload.
        It should raise ValidationErrors for all required fields.
        """
        form = CitizenEntryForm(data={})

        assert not form.is_valid()
        assert 'name' in form.errors
        assert 'cpf' in form.errors
        assert 'department' in form.errors


class TestSearchCitizenForm:
    """
    Class responsible for holding tests of 'SearchCitizenForm'.
    """

    def test_search_form_cleans_cpf_punctuation(self):
        """
        Testing if the punctuation is correctly stripped.
        It should return a digits-only string.
        """
        data = {'cpf': '123.456.789-01'}
        form = SearchCitizenForm(data=data)

        assert form.is_valid()
        assert form.cleaned_data['cpf'] == '12345678901'

    def test_search_form_is_valid_when_empty(self):
        """
        Since the CPF field is required=False, submitting an empty
        form should technically be valid and yield an empty string.
        """
        form = SearchCitizenForm(data={})

        assert form.is_valid()
        assert form.cleaned_data.get('cpf') == ''