from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('weeks', views.WeekModelViewset)
router.register('coach-class', views.CoachClassViewset)
router.register('trains', views.TrainViewset)
router.register('stations', views.StationViewset)
router.register('routes', views.RouteViewset)
router.register('schedules', views.ScheduleViewset)

urlpatterns = [
    path('', include(router.urls)),
]