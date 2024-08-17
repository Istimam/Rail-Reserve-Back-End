from rest_framework import serializers
from .models import NIDModel

class NIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIDModel
        fields = '__all__'
        # exclude = ['id_number']
