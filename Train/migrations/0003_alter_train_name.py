# Generated by Django 5.0.6 on 2024-09-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Train', '0002_remove_trainstation_station_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
