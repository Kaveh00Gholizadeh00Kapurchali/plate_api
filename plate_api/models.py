from django.db import models
from django.utils.timezone import now  # استفاده از timezone.now برای مقدار پیش‌فرض

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_plate = models.CharField(max_length=255, null=False, unique=True)
    status = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True, default='')
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد رکورد

    def __str__(self):
        return self.vehicle_plate

class License(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='licenses')
    status = models.BooleanField(null=False)

    def __str__(self):
        return f"License {self.id} for {self.vehicle.vehicle_plate}"

class TrafficHistory(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='traffic_history')
    date = models.DateTimeField(default=now)  # استفاده از now برای مقدار پیش‌فرض
    type = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"Traffic {self.type} for {self.vehicle.vehicle_plate} at {self.date}"
