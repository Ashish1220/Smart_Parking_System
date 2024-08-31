import cv2
import pickle
import cvzone
import numpy as np

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

while True:
    width, height = 195, 110

    img = cv2.imread(img_folder_path + 'Slots.png')
    
    img_height, img_width = img.shape[:2]
    print(img_height, img_width)
    
    # Define the mid-point
    mid = img_width // 2

    # Split the image into left and right halves
    slot_1 = img[:, :mid].copy()
    slot_2 = img[:, mid:].copy()

    # Create a black status box at the bottom of the image
    status_box_height = 120
    status_box_slot_1 = np.zeros((status_box_height, mid, 3), dtype=np.uint8)
    status_box_slot_2 = np.zeros((status_box_height, img_width - mid, 3), dtype=np.uint8)
    
    # Define the mode status text
    drawing_status_text = "Drawing Mode: " + ("ON" if drawing_mode else "OFF")
    nearby_available_slot_status = "Nearby Available Slot: "+ str(1)
    total_available_slot_status_1 = "Total Available Slots (Parking 1) : "+ str(10)
    total_available_slot_status_2 = "Total Available Slots (Parking 2) : "+ str(10)
    
    # Add text to the status box
    cv2.putText(status_box_slot_1, drawing_status_text+" Press 'd' to toggle", (10, status_box_height - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(status_box_slot_2, drawing_status_text+" Press 'd' to toggle", (10, status_box_height - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(status_box_slot_1, nearby_available_slot_status, (10, status_box_height - 49), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(status_box_slot_2, nearby_available_slot_status, (10, status_box_height - 49), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(status_box_slot_1, total_available_slot_status_1, (10, status_box_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(status_box_slot_2, total_available_slot_status_2, (10, status_box_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(img=slot_1, text="Exit", org=((mid//2)-70, 0+50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,0,255), thickness=2)
    cv2.putText(img=slot_1, text="Entry", org=((mid//2)-90, slot_1.shape[:2][1]-30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,255,0), thickness=2)

    cv2.putText(img=slot_2, text="Exit", org=((mid//2)-70, 0+50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,0,255), thickness=2)
    cv2.putText(img=slot_2, text="Entry", org=((mid//2)-90, slot_1.shape[:2][1]-30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0,255,0), thickness=2)

    # Draw rectangles on the slots
    for i, pos in enumerate(posList_slot_1):
        cv2.rectangle(slot_1, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        color = (255, 0, 0)
        thickness = 5
        cvzone.putTextRect(slot_1, str(i + 1), (pos[0] + 10, pos[1] + 25), scale=1.5, thickness=2, offset=5, colorR=color)
    
    for i, pos in enumerate(posList_slot_2):
        cv2.rectangle(slot_2, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        color = (255, 0, 0)
        thickness = 5
        cvzone.putTextRect(slot_2, str(i + 1), (pos[0] + 10, pos[1] + 25), scale=1.5, thickness=2, offset=5, colorR=color)

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
    # elif key == ord('c'):
    #     drawing_mode = False
    
    if cv2.getWindowProperty("PARKING 1", cv2.WND_PROP_VISIBLE) < 1 or cv2.getWindowProperty("PARKING 2", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
