# Generated by Django 5.0.6 on 2024-09-26 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Train', '0003_alter_train_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachclass',
            name='coach_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='runson',
            name='day_name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
