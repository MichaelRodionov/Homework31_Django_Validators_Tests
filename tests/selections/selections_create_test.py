import pytest


# ----------------------------------------------------------------
# ad create test
@pytest.mark.django_db
def test_create_selection(client, auth_data: tuple) -> None:
    """
    Function to create test selection and compare response with test data
    :param client: test client
    :param auth_data: tuple(auth_token, auth_id)
    :return: None
    """
    auth_token: str = auth_data[0]
    auth_id: int = auth_data[1]

    data: dict = {
        'name': 'test_selection',
        'owner': auth_id,
        'items': []
    }

    response = client.post(
        '/selection/',
        data=data,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + auth_token
    )

    expected_response: dict = {
        'id': response.data.get('id'),
        'owner': 1,
        'name': "test_selection",
        'advertisements': []
    }

    assert response.status_code == 201, 'Status code error'
    assert response.data == expected_response, 'Wrong data expected'
