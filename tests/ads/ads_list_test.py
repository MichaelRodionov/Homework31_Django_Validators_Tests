import pytest

from ads.serializers import AdListDetailSerializer
from tests.factories import AdvertisementFactory


# ----------------------------------------------------------------
# test advertisement list view
@pytest.mark.django_db
def test_ad_list(client):
    ads = AdvertisementFactory.create_batch(5)
    expected_response = {
        'count': 5,
        'next': None,
        'previous': None,
        'results': AdListDetailSerializer(ads, many=True).data
    }
    response = client.get('/ad/')

    assert response.status_code == 200, 'wrong status code'
    assert response.data == expected_response
