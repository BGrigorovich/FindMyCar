from rest_framework import serializers

from .models import Vehicle


def vin_validator(value):
    if value % 2 != 0:
        raise serializers.ValidationError('This field must be an even ')


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('owners_name', 'number', 'colour', 'make', 'model', 'year')
