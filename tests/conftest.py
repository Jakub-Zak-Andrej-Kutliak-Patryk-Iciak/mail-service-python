import pytest

from src.services import EmailService
from src import create_app, mail


@pytest.fixture(scope='module')
def test_email_service():
    return EmailService(mail)


@pytest.fixture(scope='module')
def test_client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client
