from rest_framework import viewsets
from .models import Train, RunsOn, CoachClass, Station, TrainStation
from .serializers import TrainSerializer, RunsOnSerializer, CoachClassSerializer, StationSerializer, TrainStationSerializer
from rest_framework.response import Response
from rest_framework import status

# ViewSet for the Train model

# class TrainViewSet(viewsets.ModelViewSet):
#     queryset = Train.objects.all()
#     serializer_class = TrainSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         # Create Train instance first
#         train_serializer = TrainSerializer(data=data)
#         if train_serializer.is_valid():
#             train = train_serializer.save()

#             # Create Coach Classes
#             for coach_data in data.get('coach_classes', []):
#                 coach_class, created = CoachClass.objects.get_or_create(coach_name=coach_data['coach_name'])
#                 train.coach_classes.add(coach_class)

#             # Create Runs On days
#             for run_data in data.get('runs_on', []):
#                 runs_on, created = RunsOn.objects.get_or_create(day_name=run_data['day_name'])
#                 train.runs_on.add(runs_on)

#             # Create Train Stations
#             for station_data in data.get('train_stations', []):
#                 station, created = Station.objects.get_or_create(name=station_data['station_name'])
#                 TrainStation.objects.create(
#                     train=train,
#                     station=station,
#                     arrival_time=station_data['arrival_time'],
#                     departure_time=station_data['departure_time']
#                 )

#             return Response(train_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(train_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        # Create Train instance first
        train_serializer = TrainSerializer(data=data)
        if train_serializer.is_valid():
            train = train_serializer.save()

            # Associate existing Coach Classes
            for coach_data in data.get('coach_classes', []):
                try:
                    coach_class = CoachClass.objects.get(coach_name=coach_data['coach_name'])
                    train.coach_classes.add(coach_class)
                except CoachClass.DoesNotExist:
                    return Response({'error': f"Coach class '{coach_data['coach_name']}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Associate existing Runs On days
            for run_data in data.get('runs_on', []):
                try:
                    runs_on = RunsOn.objects.get(day_name=run_data['day_name'])
                    train.runs_on.add(runs_on)
                except RunsOn.DoesNotExist:
                    return Response({'error': f"Day '{run_data['day_name']}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Associate existing Train Stations
            for station_data in data.get('train_stations', []):
                try:
                    station = Station.objects.get(name=station_data['station_name'])  # Assuming 'Station' is a separate model
                    TrainStation.objects.create(
                        train=train,
                        station_name=station.name,  # Use station name from the existing station
                        arrival_time=station_data['arrival_time'],
                        departure_time=station_data['departure_time']
                    )
                except Station.DoesNotExist:
                    return Response({'error': f"Station '{station_data['station_name']}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(train_serializer.data, status=status.HTTP_201_CREATED)
        return Response(train_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet for the RunsOn model (days of the week)
class RunsOnViewSet(viewsets.ModelViewSet):
    queryset = RunsOn.objects.all()
    serializer_class = RunsOnSerializer

# ViewSet for the CoachClass model
class CoachClassViewSet(viewsets.ModelViewSet):
    queryset = CoachClass.objects.all()
    serializer_class = CoachClassSerializer

# ViewSet for the Station model
class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class TrainStationViewSet(viewsets.ModelViewSet):
    queryset = TrainStation.objects.all()
    serializer_class = TrainStationSerializer
