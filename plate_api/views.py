from django.shortcuts import render, HttpResponse

from rest_framework.viewsets import ModelViewSet
# Import ModelViewSet from rest_framework for creating RESTful views based on models.
from .models import Vehicle
# Import the Vehicle model from your app's models.py file.
from .serializers import VehicleSerializer
# Import the VehicleSerializer created earlier in your serializers module.

from rest_framework.viewsets import ModelViewSet
# Import ModelViewSet from rest_framework for creating RESTful views based on models.
from .models import License
# Import the License model from your app's models.py file.
from .serializers import LicenseSerializer
# Import the LicenseSerializer created earlier in your serializers module.

from rest_framework.viewsets import ModelViewSet
# Import ModelViewSet from rest_framework for creating RESTful views based on models.
from .models import TrafficHistory
# Import the TrafficHistory model from your app's models.py file.
from .serializers import TrafficHistorySerializer
# Import the TrafficHistorySerializer created earlier in your serializers module.

# Create your views here.
def index(request):
    return HttpResponse("waasup!")

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all() 
    # Define the queryset for this viewset to handle all Vehicle objects.
    serializer_class = VehicleSerializer
    # Specify the serializer class that should be used for serializing and deserializing data.
    
    
class LicenseViewSet(ModelViewSet):
    queryset = License.objects.all() 
    # Define the queryset for this viewset to handle all License objects.
    serializer_class = LicenseSerializer 
    # Specify the serializer class that should be used for serializing and deserializing data.
    
    
class TrafficHistoryViewSet(ModelViewSet):
    queryset = TrafficHistory.objects.all()
    # Define the queryset for this viewset to handle all TrafficHistory objects.
    serializer_class = TrafficHistorySerializer
    # Specify the serializer class that should be used for serializing and deserializing data.