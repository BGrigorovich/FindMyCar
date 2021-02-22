from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import generics

from .models import Vehicle
from .serializers import VehicleCreateSerializer, VehicleRetrieveSerializer


class VehicleCreateUpdateAPIView(generics.CreateAPIView, UpdateModelMixin):
    serializer_class = VehicleCreateSerializer
    queryset = Vehicle.objects.all()


class VehicleListAPIView(generics.CreateAPIView, UpdateModelMixin):
    serializer_class = VehicleRetrieveSerializer
    queryset = Vehicle.objects.all()
