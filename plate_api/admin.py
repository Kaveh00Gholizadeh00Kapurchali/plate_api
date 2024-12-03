from django.contrib import admin
from .models import Vehicle, License, TrafficHistory 
# Import your model classes
from .serializers import VehicleSerializer, LicenseSerializer, TrafficHistorySerializer
# Import your serializer classes

#creating admin classes:

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_plate')  # Define which fields should be visible in the list view.
    search_fields = ['vehicle_plate']  # Enable searching by vehicle plate.
    list_filter = ('status',)  # Enable filtering by license status.

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'status')  # Define which fields should be visible in the list view.
    search_fields = ['vehicle__vehicle_plate']  # Search by vehicle plate through the related vehicle.
    list_filter = ('status',)  # Enable filtering by license status.

class TrafficHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'date', 'type')  # Define which fields should be visible in the list view.
    search_fields = ['vehicle__vehicle_plate']  # Search by vehicle plate through the related vehicle.
    list_filter = ('date',)  # Enable filtering by date.



# Register your models here.

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(TrafficHistory, TrafficHistoryAdmin) 
