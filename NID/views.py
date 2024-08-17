from rest_framework import viewsets, pagination, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import NIDModel
from .serializers import NIDSerializer

class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class NIDViewset(viewsets.ModelViewSet):
    queryset = NIDModel.objects.all()
    serializer_class = NIDSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
