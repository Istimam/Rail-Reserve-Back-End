from django.db import models

# Create your models here.
class WeekModel(models.Model):
    days = models.CharField(max_length=20)
    def __str__(self):
        return self.days

class CoachClass(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class TrainModel(models.Model):
    train_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    runs_on = models.ManyToManyField(WeekModel, null=True, blank=True)
    classes = models.ManyToManyField(CoachClass, null=True, blank=True)

    def __str__(self):
        return self.name
class Station(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    
class Route(models.Model):
    train = models.ForeignKey(TrainModel,on_delete=models.CASCADE, null=True, blank=True)
    name = models.ForeignKey(Station,on_delete=models.CASCADE, null=True, blank=True,unique=True)
    order = models.PositiveIntegerField()
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.train.name} {self.name} (Arrival  {self.arrival_time} - Departure {self.departure_time})"   


# class Schedule(models.Model):
#     train = models.ForeignKey(TrainModel, on_delete=models.CASCADE)
#     date = models.DateField()
