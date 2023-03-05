from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db.models import Model, IntegerField, CharField, \
    BooleanField, ForeignKey, CASCADE, ImageField

from authentication.models import User


# ----------------------------------------------------------------
# Category model
class Category(Model):
    name: CharField = CharField(max_length=100)
    slug: CharField = CharField(unique=True, validators=[MinLengthValidator(5), MaxLengthValidator(10)], null=True, max_length=10)

    class Meta:
        verbose_name: str = 'Категория'
        verbose_name_plural: str = 'Категории'

    def __str__(self):
        return self.name


# ----------------------------------------------------------------
# Advertisement model
class Advertisement(Model):
    name: CharField = CharField(max_length=400, null=False, validators=[MinLengthValidator(10)])
    author: ForeignKey = ForeignKey(User, on_delete=CASCADE, null=True)
    price: IntegerField = IntegerField(validators=[MinValueValidator(0)])
    description: CharField = CharField(max_length=1000, null=True)
    is_published: BooleanField = BooleanField()
    image: ImageField = ImageField(upload_to='images/', null=True)
    category: ForeignKey = ForeignKey(Category, on_delete=CASCADE, null=True)

    class Meta:
        verbose_name: str = 'Объявление'
        verbose_name_plural: str = 'Объявления'

        ordering: list[str] = ['-price']

    def __str__(self):
        return self.name
