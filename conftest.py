import pytest
from django.core.management import call_command


@pytest.fixture()
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'db.json')


@pytest.fixture
def login_data():
    data = {
        'user': {'username': 'ogksandr@gmail.com', 'password': '1234'},
        'superuser': {'username': 'soft.oganes@gmail.com', 'password': '1234'},
    }
    return data