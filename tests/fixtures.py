import pytest


@pytest.fixture()
@pytest.mark.django_db
def auth_data(client, django_user_model) -> tuple:
    """
    A fixture to add user to database, login and return valid access token
    :param client:
    :param django_user_model:
    :return: tuple with user id and access token
    """
    username = 'test_user'
    password = 'test_password123'

    user = django_user_model.objects.create_user(
        username=username,
        password=password
    )

    response = client.post(
        '/user/token/',
        {'username': username, 'password': password},
        format='json'
    )

    return response.data['access'], user.pk
