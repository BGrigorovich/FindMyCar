from rest_framework import serializers

from .models import Vehicle


class VehicleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('owners_name', 'number', 'colour', 'vin_code')


class VehicleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('owners_name', 'number', 'colour', 'make', 'model', 'year', 'vin_code')
