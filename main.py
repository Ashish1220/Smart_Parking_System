import cv2
import pickle
import cvzone
import numpy as np
import threading
import time
import pymysql
from datetime import datetime
position_folder_path = "Slot Position Pickle File/"
img_folder_path = "Image/"

try:
    with open(position_folder_path + 'CarParkPos_slot1', 'rb') as f:
        posList_slot_1 = pickle.load(f)
    
    with open(position_folder_path + 'CarParkPos_slot2', 'rb') as f:
        posList_slot_2 = pickle.load(f)

except:
    posList_slot_1 = []
    posList_slot_2 = []


drawing_mode = False  # Flag to track drawing mode
current_slot = None    # Track the slot currently being edited
width, height = 195, 110

car_present_thrshold = 1500

parking_1_status, parking_2_status = [], []

for i in range(len(posList_slot_1)):
    parking_1_status.append(True)

for i in range(len(posList_slot_2)):
    parking_2_status.append(True)

def mouseClick_slot_1(events, x, y, flags, params):
    global drawing_mode

    if drawing_mode:
        if events == cv2.EVENT_LBUTTONDOWN:
            posList_slot_1.append((x, y))
            with open(position_folder_path + 'CarParkPos_slot1', 'wb') as f:
                pickle.dump(posList_slot_1, f)
    
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList_slot_1):
                x1, y1 = pos
                if x1 < x < x1 + width and y1 < y < y1 + height:
                    posList_slot_1.pop(i)
                    with open(position_folder_path + 'CarParkPos_slot1', 'wb') as f:
                        pickle.dump(posList_slot_1, f)

def mouseClick_slot_2(events, x, y, flags, params):
    global drawing_mode

    if drawing_mode:
        if events == cv2.EVENT_LBUTTONDOWN:
            posList_slot_2.append((x, y))
            with open(position_folder_path + 'CarParkPos_slot2', 'wb') as f:
                pickle.dump(posList_slot_2, f)
    
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList_slot_2):
                x1, y1 = pos
                if x1 < x < x1 + width and y1 < y < y1 + height:
                    posList_slot_2.pop(i)
                    with open(position_folder_path + 'CarParkPos_slot2', 'wb') as f:
                        pickle.dump(posList_slot_2, f)

def checkParkingSpace(img, slotPos, parking_status):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshhold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgThreshhold, 5)

    # To make the lines Thicker in imgThreshold
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)


    spaceCounter = 0

    for idx, pos in enumerate(slotPos):
        x, y = pos

        imgCrop = imgMedian[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        if count < car_present_thrshold:
            spaceCounter += 1
            color = (0, 255, 0)
            thickness = 5
            cvzone.putTextRect(img, str(count), (x, y + height - 5), scale=1.5, thickness=2, offset=1, colorR=color)
            parking_status[idx] = True
        else:
            color = (0, 0, 255)
            thickness = 2
            cvzone.putTextRect(img, str(count), (x, y + height - 5), scale=1.5, thickness=2, offset=1, colorR=color)
            parking_status[idx] = False

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    return spaceCounter

def checkNearestSlot(parking_status):
    for i, status in enumerate(parking_status):
        if status:
            return i+1
        
    return 0

def display_parking_slots(cursor,connection):
    global drawing_mode
    

    cap = cv2.VideoCapture(1)  # 0 is usually the default camera

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 641)
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

           # Create a cursor object

        # Define the SQL query
        

        

        # print(parking_1_status)
        # print(parking_2_status)
        ret, img = cap.read()

        if not ret:
            print("Unable to get frame")
            continue

        img_height, img_width = img.shape[:2]
        # print(img_height, img_width)
        
        # Define the mid-point
        mid = img_width // 2

        # Split the image into left and right halves
        slot_1 = img[:, :mid].copy()
        slot_2 = img[:, mid:].copy()


        spaceLeft_slot1 = checkParkingSpace(slot_1, posList_slot_1, parking_1_status)
        spaceLeft_slot2 = checkParkingSpace(slot_2, posList_slot_2, parking_2_status)

        parking_1_nearest_index = checkNearestSlot(parking_1_status)
        parking_2_nearest_index = checkNearestSlot(parking_2_status)

        if elapsed_time >= 2:  # Check if 60 seconds have passed
            query = '''
        INSERT INTO `smart parking system`.`traffic` (
            `time`, 
            `available_in_parking_1`, 
            `available_in_parking_2`, 
            `nearest_in_parking_1`, 
            `nearest_in_parking_2`
        ) VALUES (
            %s, 
            %s, 
            %s, 
            %s, 
            %s
        );
        '''

            cursor.execute(query,(datetime.now(),spaceLeft_slot1,spaceLeft_slot2,parking_1_nearest_index,parking_2_nearest_index))
            connection.commit()

            start_time = current_time
        # Create a black status box at the bottom of the image
        status_box_height = 120
        status_box_slot_1 = np.zeros((status_box_height, mid, 3), dtype=np.uint8)
        status_box_slot_2 = np.zeros((status_box_height, img_width - mid, 3), dtype=np.uint8)
        
        # Define the mode status text
        drawing_status_text = "Drawing Mode: " + ("ON" if drawing_mode else "OFF")
        nearby_available_slot_status_1 = "Nearby Available Slot: "+ str(parking_1_nearest_index)
        nearby_available_slot_status_2 = "Nearby Available Slot: "+ str(parking_2_nearest_index)

        if spaceLeft_slot1 == 0:
            total_available_slot_status_1 = "Parking 1 is Full"
        else:
            total_available_slot_status_1 = "Total Available Slots (Parking 1) : "+ str(spaceLeft_slot1)
        if spaceLeft_slot2 == 0:
            total_available_slot_status_2 = "Parking 2 is Full"    
        else:
            total_available_slot_status_2 = "Total Available Slots (Parking 2) : "+ str(spaceLeft_slot2)
        
        # Add text to the status box
        cv2.putText(status_box_slot_1, drawing_status_text+" Press 'd' to toggle", (10, status_box_height - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(status_box_slot_2, drawing_status_text+" Press 'd' to toggle", (10, status_box_height - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(status_box_slot_1, nearby_available_slot_status_1, (10, status_box_height - 49), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(status_box_slot_2, nearby_available_slot_status_2, (10, status_box_height - 49), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(status_box_slot_1, total_available_slot_status_1, (10, status_box_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(status_box_slot_2, total_available_slot_status_2, (10, status_box_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(img=slot_1, text="Exit", org=((mid//2)-70, 0+50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,0,255), thickness=2)
        cv2.putText(img=slot_1, text="Entry", org=((mid//2)-90, slot_1.shape[:2][1]-30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,255,0), thickness=2)

        cv2.putText(img=slot_2, text="Exit", org=((mid//2)-70, 0+50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,0,255), thickness=2)
        cv2.putText(img=slot_2, text="Entry", org=((mid//2)-90, slot_1.shape[:2][1]-30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,255,0), thickness=2)

        # Draw rectangles on the slots
        for i, pos in enumerate(posList_slot_1):
            color = (255, 0, 0)
            thickness = 5
            cvzone.putTextRect(slot_1, str(i + 1), (pos[0] + 10, pos[1] + 25), scale=1.5, thickness=2, offset=5, colorR=color)
        
        for i, pos in enumerate(posList_slot_2):
            color = (255, 0, 0)
            thickness = 2
            cvzone.putTextRect(slot_2, str(i + 1), (pos[0] + 10, pos[1] + 25), scale=1.5, thickness=thickness, offset=5, colorR=color)

        # Combine the status box with the image slots
        slot_1_with_status = np.vstack((slot_1, status_box_slot_1))
        slot_2_with_status = np.vstack((slot_2, status_box_slot_2))

        # Display the images with the status box
        cv2.imshow('PARKING 1', slot_1_with_status)
        cv2.imshow('PARKING 2', slot_2_with_status)

        cv2.setMouseCallback('PARKING 1', mouseClick_slot_1)
        cv2.setMouseCallback('PARKING 2', mouseClick_slot_2)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            
            break
        elif key == ord('d'):
            drawing_mode = not drawing_mode
        
        if cv2.getWindowProperty("PARKING 1", cv2.WND_PROP_VISIBLE) < 1 or cv2.getWindowProperty("PARKING 2", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Create and start the thread

        # Establish a database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='smart parking system'
)
cursor = connection.cursor()

thread = threading.Thread(target=display_parking_slots(cursor,connection))


   
    
    
thread.start()

# Wait for the thread to finish
thread.join()


#   CREATE TABLE `smart_parking_system`.`traffic` (
#     `id` INT AUTO_INCREMENT,  -- Added an auto-incrementing primary key column
#     `time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Changed to TIMESTAMP for automatic current time
#     `available_in_parking_1` INT(2) NOT NULL,
#     `available_in_parking_2` INT(2) NOT NULL,
#     `nearest_in_parking_1` INT(2) NOT NULL,
#     `nearest_in_parking_2` INT(2) NOT NULL,
#     PRIMARY KEY (`id`)  -- Defined primary key column
# ) ENGINE=InnoDB;