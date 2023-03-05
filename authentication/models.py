from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ManyToManyField, TextChoices, DateField, EmailField
from rest_framework.exceptions import ValidationError

from locations.models import Location


def check_available_age(birth_date: date) -> ValidationError | None:
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 9:
        raise ValidationError(f'{age} is less than 9')


# ----------------------------------------------------------------
# User model
class User(AbstractUser):
    class Roles(TextChoices):
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        MEMBER = 'member', 'Пользователь'

    password: CharField = CharField(max_length=200)
    role: CharField = CharField(max_length=15, choices=Roles.choices, default=Roles.MEMBER)
    age: IntegerField = IntegerField(null=True)
    locations: ManyToManyField = ManyToManyField(Location, default=[])
    birth_date: DateField = DateField(null=True, validators=[check_available_age])
    email: EmailField = EmailField(null=True, unique=True)

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self):
        return self.username
