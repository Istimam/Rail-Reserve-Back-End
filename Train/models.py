from django.db import models
from django.db.models.functions import Lower
# Model for the days of the week on which the train runs
class RunsOn(models.Model):
    day_name = models.CharField(max_length=20)  # Example: "Monday", "Tuesday", etc.
    
    
    def __str__(self):
        return self.day_name


# Model for the different classes of coaches on the train
class CoachClass(models.Model):
    coach_name = models.CharField(max_length=50)  # Example: "First Class", "Second Class", etc.
   
    def __str__(self):
        return self.coach_name

# Model for the stations
class Station(models.Model):
    name = models.CharField(max_length=100)  # Station name
    
    def __str__(self):
        return self.name

# Intermediary model to represent the train's stop at each station, with arrival and departure times
class TrainStation(models.Model):
    train = models.ForeignKey('Train', on_delete=models.CASCADE, related_name='train_stations')  # Train
    station_name = models.CharField(max_length=100, default='')  # Station name
    arrival_time = models.TimeField()  # Arrival time at the station for this specific train
    departure_time = models.TimeField()  # Departure time from the station for this specific train
    
    def __str__(self):
        return f"{self.train.name} at {self.station_name}"

# Main model for the train
class Train(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the train
    coach_classes = models.ManyToManyField(CoachClass)  # Train has multiple coach classes
    runs_on = models.ManyToManyField(RunsOn)  # Train runs on multiple days of the week

    def __str__(self):
        return self.name
