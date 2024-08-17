from django.core.validators import RegexValidator
from django.db import models
from .constants import GENDER_TYPE
import random

class NIDModel(models.Model):
    id_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex='^\d{10,15}$',
                message='ID number must be between 10 and 15 digits.'
            )
        ],
        unique=True
    )
    id_name = models.CharField(max_length=30)
    id_gender = models.CharField(max_length=100, choices=GENDER_TYPE)
    id_father_name = models.CharField(max_length=30)
    id_mother_name = models.CharField(max_length=30)
    id_date_of_birth = models.DateField()
    id_address = models.CharField(max_length=300)
    id_photo = models.ImageField(upload_to='nid_photos/')

    def save(self, *args, **kwargs):
        if not self.id_number:
            dob_str = self.id_date_of_birth.strftime('%Y%m%d')
            random_number = random.randint(1000, 9999)
            self.id_number = f"{dob_str}{random_number}"

            while NIDModel.objects.filter(id_number=self.id_number).exists():
                random_number = random.randint(1000, 9999)
                self.id_number = f"{dob_str}{random_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_number} {self.id_name}"
