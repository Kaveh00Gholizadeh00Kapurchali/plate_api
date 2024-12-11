from django.shortcuts import render, HttpResponse
import requests
import urllib.request
from rest_framework.response import Response

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

#open cv imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Vehicle, License
from .serializers import VehicleSerializer, LicenseSerializer
import cv2
from ultralytics import YOLO


# Create your views here.

# تابع برای شناسایی پلاک
def read_plate(img):
    try:
        # بارگذاری مدل YOLO برای شناسایی پلاک و مدل برای شناسایی کاراکترها
        ymodel = YOLO("best.pt")  # مدل YOLO برای شناسایی پلاک خودرو
        nmodel = YOLO("best_char2.pt")  # مدل YOLO برای شناسایی کاراکترهای پلاک

        # پردازش تصویر و شناسایی پلاک‌ها
        results = ymodel(img)  # شناسایی پلاک‌ها در تصویر
        res_plotted = results[0].plot()  # رسم نتایج بر روی تصویر (برای نمایش)

        # استخراج جعبه‌های محدودکننده برای پلاک‌ها
        boxes = results[0].boxes.xyxy.tolist()

        # جستجو در جعبه‌ها و برش تصویر پلاک
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            plate_img = img[int(y1):int(y2), int(x1):int(x2)]  # برش پلاک از تصویر

        # شناسایی کاراکترها در پلاک
        char_results = nmodel(plate_img)  # شناسایی کاراکترها با مدل YOLO مخصوص کاراکتر
        if len(char_results[0].boxes) > 0:
            detected_characters = []
            char_bboxes = []  # لیستی برای ذخیره جعبه‌های محدودکننده کاراکترها
            for c_box in char_results[0].boxes:
                label = char_results[0].names[int(c_box.cls)]  # برچسب کاراکتر
                x_coord = c_box.xyxy[0][0]  # مختصات X برای مرتب‌سازی
                detected_characters.append((x_coord, label))  # ذخیره کاراکتر و مختصات آن
                char_bbox = list(map(int, c_box.xyxy[0]))  # ذخیره جعبه محدودکننده کاراکتر
                char_bboxes.append(char_bbox)

            # مرتب‌سازی کاراکترها بر اساس مختصات X (برای ساخت پلاک کامل)
            detected_characters.sort(key=lambda x: x[0])
            # استخراج متن پلاک از کاراکترهای شناسایی‌شده
            number = ""
            i = 0
            for char in detected_characters:
                if i == 6:  # افزودن "IRAN:" بعد از شش کاراکتر اول
                    number += " IRAN:"
                number += "".join(char[1])  # اضافه کردن کاراکتر به متن پلاک
                i += 1

        return number  # بازگشت پلاک شناسایی‌شده
    except Exception as e:
        # در صورت بروز خطا، پیغام خطا برمی‌گرداند
        return f"error => {str(e)}"

# ایجاد ViewSet برای شناسایی پلاک
class VehiclePlateRecognitionViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)  # برای دریافت فایل‌های تصویر از نوع multipart
    
    @action(detail=False, methods=['post'])
    def recognize_plate(self, request):
        """
        شناسایی پلاک خودرو از تصویر و ذخیره آن در پایگاه داده.
        """
        file = request.data.get('image')  # دریافت فایل تصویر از درخواست

        if file:
            # ذخیره تصویر در مسیر موقت
            with open('uploaded_image.jpg', 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            # بارگذاری تصویر با OpenCV
            image = cv2.imread('uploaded_image.jpg')

            # شناسایی پلاک
            plate_number = read_plate(image)

            # ایجاد یا بروزرسانی مدل Vehicle با پلاک شناسایی شده
            if plate_number and plate_number != "error => 0":
                vehicle, created = Vehicle.objects.get_or_create(vehicle_plate=plate_number)  # ایجاد یا بروزرسانی خودرو
                
                # ایجاد مجوز برای خودرو
                license = License.objects.create(vehicle=vehicle, status=True)

                # بازگشت اطلاعات خودرو و مجوز به کاربر
                vehicle_serializer = VehicleSerializer(vehicle)
                license_serializer = LicenseSerializer(license)
                
                return Response({
                    'vehicle': vehicle_serializer.data,
                    'license': license_serializer.data
                })
            else:
                return Response({'error': 'Plate recognition failed'}, status=400)  # در صورت شکست شناسایی پلاک
        
        return Response({'error': 'No image provided'}, status=400)  # در صورت عدم ارسال تصویر

def index(request):
    return HttpResponse("waasup!")

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all() 
    # Define the queryset for this viewset to handle all Vehicle objects.
    serializer_class = VehicleSerializer
    # Specify the serializer class that should be used for serializing and deserializing data.
    parser_classes = (MultiPartParser, FormParser)  # برای پذیرش فایل‌های آپلود شده

    def create(self, request, *args, **kwargs):
        """
        آپلود تصویر و ایجاد رکورد جدید.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # ذخیره اطلاعات در پایگاه داده
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
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