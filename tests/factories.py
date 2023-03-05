import factory

from ads.models import Advertisement, Category
from authentication.models import User


# ----------------------------------------------------------------
# instance factories
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username: factory.Faker = factory.Faker('name')
    password: str = 'test_password'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name: factory.Faker = factory.Faker('name')
    slug: factory.Faker = factory.Faker('slug')


class AdvertisementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advertisement

    name: str = 'test_advertisement'
    author: factory.SubFactory(UserFactory)
    price: int = 1000
    description: str = 'test description'
    is_published: bool = False
    image: None = None
    category: factory.SubFactory(CategoryFactory)
