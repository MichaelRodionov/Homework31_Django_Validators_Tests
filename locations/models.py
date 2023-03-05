from django.db.models import Model, CharField, DecimalField


# ----------------------------------------------------------------
# Location model
class Location(Model):
    name: CharField = CharField(max_length=50)
    lat: DecimalField = DecimalField(max_digits=10, decimal_places=6, null=True)
    lng: DecimalField = DecimalField(max_digits=10, decimal_places=6, null=True)

    class Meta:
        verbose_name: str = 'Локация'
        verbose_name_plural: str = 'Локации'

    def __str__(self):
        return self.name
