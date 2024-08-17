# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator,MinLengthValidator, MaxLengthValidator
from rest_framework.validators import UniqueValidator
from NID.models import NIDModel

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    nid_number = serializers.CharField(
        write_only=True, 
        required=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Field must only contain digits.'
            ),
            MinLengthValidator(10),
            MaxLengthValidator(15)
        ],
    )
    date_of_birth = serializers.DateField(write_only=True, required=True)
    postal_code = serializers.CharField(write_only=True, required=True)
    address = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('phone_no','nid_number','date_of_birth','email','postal_code','address', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        try:
            nid = NIDModel.objects.get(id_number=attrs['nid_number'], id_date_of_birth=attrs['date_of_birth'])
            attrs['username'] = nid.id_name
        except NIDModel.DoesNotExist:
            raise serializers.ValidationError({"nid_number": "NID number and date of birth do not match."})

        if not attrs.get('address'):
            raise serializers.ValidationError({"address": "This field may not be blank."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        username = validated_data.pop('username')
        user = User.objects.create(
            phone_no=validated_data['phone_no'],
            username=username,
            email=validated_data['email'],
            nid_number=validated_data['nid_number'],  # Save nid_number in the user model
            date_of_birth=validated_data['date_of_birth'] , # Save date_of_birth in the user model
            postal_code=validated_data['postal_code'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone_no = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','nid_number', 'phone_no', 'username', 'email', 'postal_code', 'address', 'is_active', 'is_staff', 'date_joined']
        # fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_no', 'email', 'postal_code', 'address')

    def validate(self, attrs):
        if not attrs.get('address'):
            raise serializers.ValidationError({"address": "This field may not be blank."})
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs
