from rest_framework import serializers
from .models import RunsOn, CoachClass, Station, Train, TrainStation

# Serializer for the days of the week
class RunsOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunsOn
        fields = ['day_name']

# Serializer for the coach classes
class CoachClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachClass
        fields = ['coach_name']

# Serializer for the stations
class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['name']

# Serializer for the intermediary model to include train's specific stop at each station
class TrainStationSerializer(serializers.ModelSerializer):
    # Directly use the station_name field instead of a nested serializer
    class Meta:
        model = TrainStation
        fields = ['station_name', 'arrival_time', 'departure_time', 'train']

# Serializer for the train, including all related data
class TrainStationSerializer(serializers.ModelSerializer):
    # Remove the train field from being exposed to the frontend
    class Meta:
        model = TrainStation
        fields = ['station_name', 'arrival_time', 'departure_time']  # Exclude 'train' field

class TrainSerializer(serializers.ModelSerializer):
    coach_classes = CoachClassSerializer(many=True)  # Nested coach classes
    runs_on = RunsOnSerializer(many=True)  # Nested days of the week
    train_stations = TrainStationSerializer(many=True)  # Nested train-station relationships
    
    class Meta:
        model = Train
        fields = ['name', 'coach_classes', 'runs_on', 'train_stations']

    def create(self, validated_data):
        stations_data = validated_data.pop('train_stations')
        coach_classes_data = validated_data.pop('coach_classes')
        runs_on_data = validated_data.pop('runs_on')

        # Create Train instance
        train = Train.objects.create(**validated_data)

        # Associate Coach Classes
        for coach_data in coach_classes_data:
            coach_class = CoachClass.objects.get(coach_name=coach_data['coach_name'])
            train.coach_classes.add(coach_class)

        # Associate Run Days
        for run_data in runs_on_data:
            runs_on = RunsOn.objects.get(day_name=run_data['day_name'])
            train.runs_on.add(runs_on)

        # Create Train Stations and associate them with the train
        # for station_data in stations_data:
        #     TrainStation.objects.create(
        #         train=train,
        #         station_name=station_data['station_name'],
        #         arrival_time=station_data['arrival_time'],
        #         departure_time=station_data['departure_time']
        #     )
        for station_data in stations_data:
            # Just ensure the `train` field is set without creating duplicates
            # This assumes `TrainStation` records already exist and you are updating them
            TrainStation.objects.filter(
                station_name=station_data['station_name'],  # Adjust this filter based on your needs
                arrival_time=station_data['arrival_time'],
                departure_time=station_data['departure_time']
            ).update(train=train)
        return train
