from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NIDViewset

router = DefaultRouter()
router.register('list', NIDViewset)

urlpatterns = [
    path('', include(router.urls)),
]
