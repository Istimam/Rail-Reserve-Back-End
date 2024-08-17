from django.contrib import admin
from .models import TrainModel, WeekModel, Station, CoachClass, Route
# Register your models here.
admin.site.register(TrainModel)
admin.site.register(WeekModel)
admin.site.register(Station)
admin.site.register(CoachClass)
admin.site.register(Route)