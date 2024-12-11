from rest_framework import serializers

#importing local models
from .models import Vehicle
from .models import License
from .models import TrafficHistory

class VehicleSerializer(serializers.ModelSerializer):
    # Serializer for the Vehicle model
    class Meta:
        model = Vehicle  # The model that this serializer is associated with
        fields = ['id', 'vehicle_plate', "image_url", 'image']  # The specific fields to include in the serialized output

class LicenseSerializer(serializers.ModelSerializer):
    # Nested serializer for the Vehicle model
    vehicle = VehicleSerializer(read_only=True, many=False)  # Represents the related Vehicle object in a read-only format

    class Meta:
        model = License  # The model that this serializer is associated with
        fields = ['id', 'vehicle', 'status']  # The specific fields to include in the serialized output

class TrafficHistorySerializer(serializers.ModelSerializer):
    # Nested serializer for the Vehicle model
    vehicle = VehicleSerializer(read_only=True, many=False)  # Represents the related Vehicle object in a read-only format

    class Meta:
        model = TrafficHistory  # The model that this serializer is associated with
        fields = ['id', 'vehicle', 'date', 'type']  # The specific fields to include in the serialized output
