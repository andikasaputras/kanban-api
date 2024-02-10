import pytest
from app import create_app
from app.db import db


@pytest.fixture(scope='module')
def test_client():
    app = create_app('test')  # Create the app with the test configuration
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    db.drop_all()
    ctx.pop()


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='module')
def user_created(test_client):
    new_user = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }
    test_client.post('/auth/register', json=new_user)

    yield test_client  # this is where the testing happens!

    with test_client.session_transaction() as sess:
        sess.clear()
