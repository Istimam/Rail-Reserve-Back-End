from django.contrib import admin
from .models import Train, RunsOn, CoachClass, Station, TrainStation

# Inline for the TrainStation (intermediary model) to show the station stops on the Train admin page
class TrainStationInline(admin.TabularInline):
    model = TrainStation
    extra = 1  # Number of empty forms to show for adding related TrainStation objects

# Admin configuration for the Train model
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display train name in list view
    inlines = [TrainStationInline]  # Add the TrainStation inline to show station stops

# Admin configuration for the RunsOn model (days of the week)
class RunsOnAdmin(admin.ModelAdmin):
    list_display = ('day_name',)  # Display day name in list view

# Admin configuration for the CoachClass model
class CoachClassAdmin(admin.ModelAdmin):
    list_display = ('coach_name',)  # Display coach name in list view

# Admin configuration for the Station model
class StationAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display station name in list view

# Register the models with their respective admin configurations
admin.site.register(Train, TrainAdmin)
admin.site.register(RunsOn, RunsOnAdmin)
admin.site.register(CoachClass, CoachClassAdmin)
admin.site.register(Station, StationAdmin)
