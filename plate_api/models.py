from django.db import models

class Vehicle(models.Model):
    # Auto-incrementing primary key
    id = models.AutoField(primary_key=True)
    # Character field with a maximum length of 255 characters for vehicle plate number
    vehicle_plate = models.CharField(max_length=255, null=False, unique=True)
    status = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='vehicle_images/')  # ذخیره تصاویر در پوشه vehicle_images/
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # Human-readable string representation
        return self.vehicle_plate

class License(models.Model):
    # Auto-incrementing primary key
    id = models.AutoField(primary_key=True)
    # Foreign key referencing the Vehicle model
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='licenses')
    # Boolean field indicating the status of the license
    status = models.BooleanField(null=False)

    def __str__(self):  # Human-readable string representation
        return f"License {self.id} for {self.vehicle.vehicle_plate}"

class TrafficHistory(models.Model):
    # Auto-incrementing primary key
    id = models.AutoField(primary_key=True)
    # Foreign key referencing the Vehicle model
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='traffic_history')
    # Date and time field for when the event occurred
    date = models.DateTimeField(null=False)
    # Character field with a maximum length of 255 characters indicating whether it's an "Entry" or "Exit"
    type = models.CharField(max_length=255, null=False)

    def __str__(self):  # Human-readable string representation
        return f"Traffic {self.type} for {self.vehicle.vehicle_plate} at {self.date}"
