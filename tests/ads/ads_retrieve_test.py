import pytest


# ----------------------------------------------------------------
# advertisement retrieve view test
@pytest.mark.django_db
def test_retrieve_ad(client, advertisement, auth_data):
    auth_token = auth_data[0]
    expected_response = {
        'name': 'test_advertisement',
        'price': 1000,
        'description': 'test description',
        'is_published': False,
        'author': None,
        'category': None,
        'image': None,
    }

    response = client.get(
        f'/ad/{advertisement.pk}/',
        HTTP_AUTHORIZATION='Bearer ' + auth_token
    )
    assert response.status_code == 200
    assert response.data == expected_response
