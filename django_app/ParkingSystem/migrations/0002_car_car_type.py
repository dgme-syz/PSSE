# Generated by Django 4.1 on 2023-09-28 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_type',
            field=models.CharField(default='小型车', max_length=255),
        ),
    ]