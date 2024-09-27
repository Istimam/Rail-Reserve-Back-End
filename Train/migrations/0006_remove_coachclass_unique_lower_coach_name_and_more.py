# Generated by Django 5.0.6 on 2024-09-27 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Train', '0005_coachclass_unique_lower_coach_name_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='coachclass',
            name='unique_lower_coach_name',
        ),
        migrations.RemoveConstraint(
            model_name='runson',
            name='unique_lower_day_name',
        ),
        migrations.RemoveConstraint(
            model_name='station',
            name='unique_lower_station_name',
        ),
        migrations.AlterField(
            model_name='coachclass',
            name='coach_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='runson',
            name='day_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
