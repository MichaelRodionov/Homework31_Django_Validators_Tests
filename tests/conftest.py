from pytest_factoryboy import register

from tests.factories import *

# ----------------------------------------------------------------
# fixtures
pytest_plugins = 'tests.fixtures'


# ----------------------------------------------------------------
# register factories
register(UserFactory)
register(CategoryFactory)
register(AdvertisementFactory)
