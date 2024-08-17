from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator,MinLengthValidator, MaxLengthValidator
from django.utils.timezone import now
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_no, password=None, **extra_fields):
        if not phone_no:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_no, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_no = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='Phone number must be 11 digits long and contain only numbers.'
            ),
            MinLengthValidator(11),  # Must be exactly 11 digits long
            MaxLengthValidator(11)
        ]
    )
    username = models.CharField(max_length=30, default='default_username')  # Ensure unique=True is removed
    email = models.EmailField(unique=True, blank=True, null=True)
    nid_number = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='Field must only contain digits.'
            ),
            MinLengthValidator(10),
            MaxLengthValidator(15)
        ],
        unique=True
    )  # Add this field
    date_of_birth = models.DateField(null=True,
        blank=True,default=now)  # Add this field
    postal_code = models.CharField(max_length=10, default='0000')
    address = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_no

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
