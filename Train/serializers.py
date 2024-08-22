from rest_framework import serializers
from .import models
class WeekModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeekModel
        fields = '__all__'

class CoachClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoachClass
        fields = '__all__'

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrainModel
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = '__all__'
        