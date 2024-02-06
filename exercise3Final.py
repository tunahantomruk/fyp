import cv2
import numpy as np
import time

def detect_blue_objects(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    largest_contour = None
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)

    return frame, largest_contour

def detect_faces(frame):

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    face_center = None

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        face_center = (int(x + w / 2), int(y + h / 2))
        cv2.circle(frame, face_center, 7, (255, 255, 255), -1)

    return frame, faces, face_center

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

start_time = None
rest_start_time = None
exercise_count = 0
relaxing = False
reset_timer = False

while True:
    ret, frame = cap.read()

    frame = cv2.resize(frame, (640, 480))


    frame_with_blue_contours, largest_blue_contour = detect_blue_objects(frame.copy())

    frame_with_faces, faces, face_center = detect_faces(frame_with_blue_contours)

    if largest_blue_contour is not None and face_center is not None:
        M_blue = cv2.moments(largest_blue_contour)
        if M_blue["m00"] != 0:
            cx_blue = int(M_blue["m10"] / M_blue["m00"])
            cy_blue = int(M_blue["m01"] / M_blue["m00"])

                                    
            distance_to_face_blue = np.sqrt((cx_blue - face_center[0])**2 + (cy_blue - face_center[1])**2)

            

            #check posture is correct
            if distance_to_face_blue < 150:
                in_correct_posture = True
                if not relaxing:
                    if start_time is None or reset_timer:
                        start_time = time.time()
                        reset_timer = False

                    elapsed_time = time.time() - start_time

                    exercise_countdown = 10 - int(elapsed_time)
                    cv2.putText(frame_with_faces, f'Exercise: {exercise_count + 1} - Countdown: {exercise_countdown}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    if exercise_count >= 2 and exercise_count < 3:
                        cv2.putText(frame_with_faces, f'Change Sides After 3rd exercise', 
                                    (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                                    (0, 0, 255), 2)

                        
                    if elapsed_time >= 10:
                        exercise_count += 1
                        start_time = None
                        in_correct_posture = False 
                        relaxing = True
                        rest_start_time = time.time()
            else:
                #reset timer if posture is false
                in_correct_posture = False
                reset_timer = True
                start_time = None
                relaxing = False
                cv2.putText(frame_with_faces, f'Put your hand on the side of your head', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    #5seconds
    if relaxing:
        relax_elapsed_time = time.time() - rest_start_time
        cv2.putText(frame_with_faces, f'Relax for 5 seconds: {relax_elapsed_time:.2f}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if relax_elapsed_time >= 5:
            relaxing = False
            
            start_time = None

        
            if exercise_count >= 6:
                break

    cv2.imshow('Frame with Detection', frame_with_faces)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
