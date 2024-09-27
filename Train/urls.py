from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TrainViewSet, CoachClassViewSet, RunsOnViewSet, StationViewSet, TrainStationViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('trains', TrainViewSet)
router.register('coach-classes', CoachClassViewSet)
router.register('runs-on', RunsOnViewSet)
router.register('stations', StationViewSet)
router.register('add_stations', TrainStationViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

