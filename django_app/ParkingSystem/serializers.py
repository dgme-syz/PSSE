from rest_framework import serializers
from ParkingSystem.models import Car, ParkingRecord, ParkingRate, GlobalSettings


class GlobalSettingsSerializer(serializers.Serializer):
    class Meta:
        model = GlobalSettings
        fields = '__all__'


class ParkingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRecord
        fields = '__all__'


class ParkingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRate
        fields = '__all__'


class ResetParkingDurationSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(max_length=10)

    class Meta:
        model = Car
        fields = ['license_plate']


class DeleteCarSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(max_length=10)

    class Meta:
        model = Car
        fields = ['license_plate']


class ParkCarSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(max_length=10)

    class Meta:
        model = Car
        fields = ['license_plate']


class AddCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['license_plate', 'car_type']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
