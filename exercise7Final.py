import cv2
from math import sin, cos, radians
import time

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face = cv2.CascadeClassifier("haar/haarcascade_frontalface_alt2.xml")

# Set up face detection parameters
settings = {
    'scaleFactor': 1.3,
    'minNeighbors': 6,
    'minSize': (50, 50),
    'flags': cv2.CASCADE_FIND_BIGGEST_OBJECT | cv2.CASCADE_DO_ROUGH_SEARCH
}

left_rep_count = 0  
right_rep_count = 0  
rep_start_time = 0  
hold_start_time = 0  
hold_duration = 5  

def rotate_image(image, angle):
    height, width, _ = image.shape
    center_of_image = (width / 2, height / 2)
    #define matrix
    rot_mat = cv2.getRotationMatrix2D(center_of_image, angle, 0.9)
    #matrixi uygula
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)#delete flag
    return result

def rotate_point(pos, img, angle):
    x = pos[0] - img.shape[1] * 0.4
    y = pos[1] - img.shape[0] * 0.4
    newx = x * cos(radians(angle)) + y * sin(radians(angle)) + img.shape[1] * 0.4
    newy = -x * sin(radians(angle)) + y * cos(radians(angle)) + img.shape[0] * 0.4
    #x,y,w,h
    return int(newx), int(newy), pos[2], pos[3]

while True:
    ret, img = camera.read()

    
    for angle in range(-60, 61, 5):
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        #when detcted at least 1 face
        if detected is not None and len(detected) > 0:
            #last face
            detected = [rotate_point(detected[-1], img, -angle)]
            break

    
    for x, y, w, h in detected[-1:]:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Check if the head tilt angle is within the specified range
        current_angle = angle + 5
        if -40 <= current_angle <= -25:
            if rep_start_time == 0:
                rep_start_time = time.time()  #start time
                hold_start_time = time.time()  

        elif 25 <= current_angle <= 40:
            if rep_start_time == 0:
                rep_start_time = time.time()  
                hold_start_time = time.time()  

        else:
            rep_start_time = 0  

       
        if rep_start_time != 0:
            cv2.putText(img, f'Time: {round(time.time() - hold_start_time, 1)}s', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # check for hold
            if time.time() - hold_start_time >= hold_duration:
                if -40 <= current_angle <= -25:
                    left_rep_count += 1
                elif 25 <= current_angle <= 40:
                    right_rep_count += 1

                print(f'Left Rep: {left_rep_count}, Right Rep: {right_rep_count}')

        

                rep_start_time = 0 
                hold_start_time = 0  

    if left_rep_count >= 3 and right_rep_count >= 3:
        break
    cv2.putText(img, f'Angle: {abs(current_angle)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f'Left Rep: {left_rep_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f'Right Rep: {right_rep_count}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
    cv2.imshow('facedetect', img)
    
    key = cv2.waitKey(5)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
