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

class ResetParkingDurationSerializer(serializers.Serializer):
    license_plate = serializers.CharField(max_length=10)

class DeleteCarSerializer(serializers.Serializer):
    license_plate = serializers.CharField(max_length=10)

class ParkCarSerializer(serializers.Serializer):
    license_plate = serializers.CharField(max_length=10)

class AddCarSerializer(serializers.Serializer):
    class Meta:
        model = Car
        fields = '__all__'