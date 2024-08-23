from rest_framework import serializers
from .models import NIDModel
import random

class NIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIDModel
        fields = ['id_number','id_name', 'id_gender', 'id_father_name', 'id_mother_name', 'id_date_of_birth', 'id_address', 'id_photo']
        # exclude = ['id_number']  # You might exclude 'id_number' if you want to let the serializer handle it
        read_only_fields = ['id_number']

    def create(self, validated_data):
        # Generate unique ID number
        dob_str = validated_data.get('id_date_of_birth').strftime('%Y%m%d')
        random_number = random.randint(1000, 9999)
        id_number = f"{dob_str}{random_number}"

        while NIDModel.objects.filter(id_number=id_number).exists():
            random_number = random.randint(1000, 9999)
            id_number = f"{dob_str}{random_number}"

        # Add the generated ID number to validated_data
        validated_data['id_number'] = id_number

        # Create and return the NIDModel instance
        return super().create(validated_data)
