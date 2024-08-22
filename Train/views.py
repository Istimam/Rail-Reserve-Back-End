from django.shortcuts import render
from rest_framework import viewsets
from .import models
from .import serializers
# Create your views here.
class WeekModelViewset(viewsets.ModelViewSet):
    queryset = models.WeekModel.objects.all()
    serializer_class = serializers.WeekModelSerializer

class CoachClassViewset(viewsets.ModelViewSet):
    queryset = models.CoachClass.objects.all()
    serializer_class = serializers.CoachClassSerializer

class TrainViewset(viewsets.ModelViewSet):
    queryset = models.TrainModel.objects.all()
    serializer_class = serializers.TrainSerializer

class StationViewset(viewsets.ModelViewSet):
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer

class RouteViewset(viewsets.ModelViewSet):
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer

class ScheduleViewset(viewsets.ModelViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
