from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from vininfo import Vin
from vininfo.exceptions import ValidationError as VinValidationError


def validate_vin_code(value):
    try:
        Vin.validate(value)
    except VinValidationError as e:
        raise ValidationError(
            _(e.message),
            params={'value': value},
        )


class Manufacturer(models.Model):
    name = models.TextField(max_length=50, unique=True)


class CarModel(models.Model):
    manufacturer = models.ForeignKey(to=Manufacturer, on_delete=models.PROTECT)
    name = models.TextField()

    class Meta:
        unique_together = ('manufacturer', 'name')


class Vehicle(models.Model):
    owners_name = models.TextField(max_length=60)
    registration_number = models.TextField(max_length=10)
    colour = models.TextField(max_length=20)
    model = models.ForeignKey(to=CarModel, on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField()
    vin_code = models.TextField(max_length=17, validators=(validate_vin_code,))

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     vin_info = Vin(self.vin_code)
    #     country = vin_info.country
    #     year = vin_info.years[0] # todo: ask
    #     model = vin_info

    class Meta:
        unique_together = ('owners_name', 'vin_code')
