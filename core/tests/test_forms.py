import pytest
from datetime import date
from model_bakery import baker
from ..forms import CitizenEntryForm, SearchCitizenForm
from faker import Faker

fake = Faker('pt_BR')

def generate_random_data():
    """
    Generates random data for testing the form.
    It returns:

    {
        'name': random_name,
        'cpf': random_cpf,
        'birth_date': random_date,
        'phone_number': random_phone_number, 
    }
    """

    ddd = fake.random_number(digits=2, fix_len=True)
    number = fake.random_number(digits=8, fix_len=True)

    return {
        'name': fake.name().lower(),
        'cpf': fake.cpf(),
        'birth_date': fake.date(pattern="%d/%m/%Y"),
        'phone_number': f"{ddd} 9{number}", 
    }

@pytest.mark.django_db
class TestCitizenEntryForm:
    """
    Class responsible for holding tests of 'CitzenEntryForm'.
    """

    @pytest.mark.parametrize('_', range(10))
    def test_form_is_valid_with_good_data(self, _):
        """
        Testing form when all the data is valid.
        It should clean all the inputs and not throw any errors.
        """

        department = baker.make('core.Department', is_available=True)
        data = generate_random_data()
        data['department'] = department.id
        
        form = CitizenEntryForm(data=data)
        
        assert form.is_valid()


    def test_form_is_valid_with_bad_cpf(self):
        """
        Testing form when the CPF is invalid, but all the other data is valid.
        It should raise an ValidationError.
        """

        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'jose alencar silva',
            'cpf': '111.111.111-11',
            'birth_date': '20/05/1990',
            'phone_number': '61 988887777',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)
        
        assert not form.is_valid()
        assert 'cpf' in form.errors


    def test_form_is_valid_with_future_birth_date(self):
        """
        Testing form when the birth date is in the future, but all the other data is valid.
        It should raise an ValidationError.
        """

        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'jose alencar silva',
            'cpf': '654.811.380-26',
            'birth_date': '20/05/3099',
            'phone_number': '61 988887777',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)
        
        assert not form.is_valid()
        assert 'birth_date' in form.errors


    def test_form_is_valid_with_birth_date_in_invalid_format(self):
        """
        Testing form when the birth date is the invalid format, but all the other data is valid.
        It should raise an ValidationError.
        """

        department = baker.make('core.Department', is_available=True)

        data = {
            'name': 'jose alencar silva',
            'cpf': '654.811.380-26',
            'birth_date': '21-11-2001',
            'phone_number': '61 988887777',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)
        
        assert not form.is_valid()
        assert 'birth_date' in form.errors


    def test_form_is_valid_with_invalid_phone_number(self):
        """
        Testing form when the birth date is the invalid format, but all the other data is valid.
        It should raise an ValidationError.
        """

        department = baker.make('core.Department', is_available=True)
        
        data = {
            'name': 'jose alencar silva',
            'cpf': '654.811.380-26',
            'birth_date': '20/05/1990',
            'phone_number': '61 123',
            'department': department.id
        }

        form = CitizenEntryForm(data=data)
        
        assert not form.is_valid()
        assert 'phone_number' in form.errors
 

class TestSearchCitizenForm:
    """
    Class responsible for holding tests of 'SearchCitizenForm'.
    """

    def test_search_form_cleans_cpf(self):
        """
        Testing if the punctuation is correctly cleaned.
        It should should return a numbers-only string.
        """

        data = {'cpf': '123.456.789-01'}
        form = SearchCitizenForm(data=data)
        
        assert form.is_valid()
        assert form.cleaned_data['cpf'] == '12345678901'