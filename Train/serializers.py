from rest_framework import serializers
from . import models

class WeekModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeekModel
        fields = '__all__'

class CoachClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoachClass
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(queryset=models.Station.objects.all())

    class Meta:
        model = models.Route
        fields = ['id', 'name', 'order', 'arrival_time', 'departure_time']

class TrainSerializer(serializers.ModelSerializer):
    stations = RouteSerializer(many=True, source='routes')
    runs_on = serializers.PrimaryKeyRelatedField(queryset=models.WeekModel.objects.all(), many=True)
    classes = serializers.PrimaryKeyRelatedField(queryset=models.CoachClass.objects.all(), many=True)

    class Meta:
        model = models.TrainModel
        fields = ['name', 'stations', 'runs_on', 'classes']
        read_only_fields = ['train_id']
    def create(self, validated_data):
        stations_data = validated_data.pop('routes')
        runs_on_data = validated_data.pop('runs_on')
        classes_data = validated_data.pop('classes')

        train = models.TrainModel.objects.create(**validated_data)
        
        for station_data in stations_data:
            models.Route.objects.create(train=train, **station_data)
        
        train.runs_on.set(runs_on_data)
        train.classes.set(classes_data)
        
        return train



class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = '__all__'
