import cv2                       
from ultralytics import YOLO     # To Create Yolo model

###############################################################################################################
def read_plate(img):
    try:
        ymodel = YOLO("best.pt")
        nmodel = YOLO("best_char2.pt")

        results = ymodel(img)
        res_plotted = results[0].plot()

        # Extract bounding boxes
        boxes = results[0].boxes.xyxy.tolist()

        # Iterate through the bounding boxes
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            # Crop the object using the bounding box coordinates
            plate_img = img[int(y1):int(y2), int(x1):int(x2)]
            # Save the cropped object as an image
        ####################################################### after this line we start char detection
        char_results = nmodel(plate_img)
        if len(char_results[0].boxes) > 0:
            detected_characters = []
            char_bboxes = []  # List to store all character bounding boxes
            for c_box in char_results[0].boxes:
                label = char_results[0].names[int(c_box.cls)]  # Character label
                x_coord = c_box.xyxy[0][0]  # X-coordinate for sorting
                detected_characters.append((x_coord, label))
                # Store bounding box coordinates for this character
                char_bbox = list(map(int, c_box.xyxy[0]))
                char_bboxes.append(char_bbox)
            # Sort characters based on their x-coordinates
            detected_characters.sort(key=lambda x: x[0])
            # Extract the sorted text
            number=""
            i = 0
            for char in detected_characters:
                if i==6:
                    number+=" IRAN:"
                number+=("".join(char[1]))
                i+=1

        ###############################################################################
        
        return number
    except:
        return "error => 0"  
###############################################################################################################

# example of usage 
#image = cv2.imread("t13.jpg")
#print(read_plate(image))





