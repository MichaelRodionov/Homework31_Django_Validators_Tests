import pytest

from ads.models import Category


# ----------------------------------------------------------------
# ad create test
@pytest.mark.django_db
def test_create_ad(client, auth_data: tuple) -> None:
    """
    Function to create test advertisement and compare response with test data
    :param client: test client
    :param auth_data: tuple(auth_token, auth_id)
    :return: None
    """
    auth_token: str = auth_data[0]
    auth_id: int = auth_data[1]

    category: Category = Category.objects.create(
        name='test_category',
        slug='test_slug'
    )

    data: dict = {
        'name': 'test_advertisement',
        'price': 1000,
        'description': 'test description',
        'is_published': False,
        'author': 1,
        'category': 1
    }

    response = client.post(
        '/ad/',
        data=data,
        content_type='application/json',
        HTTP_AUTHORIZATION='Bearer ' + auth_token
    )

    expected_response: dict = {
        'id': response.data.get('id'),
        'image': None,
        'locations': [],
        'is_published': False,
        'name': 'test_advertisement',
        'price': 1000,
        'description': 'test description',
        'author': auth_id,
        "category": category.pk
    }

    assert response.status_code == 201, 'Status code error'
    assert response.data == expected_response, 'Wrong data expected'
