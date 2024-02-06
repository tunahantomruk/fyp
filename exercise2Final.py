import cv2
import numpy as np
import time

# color detect and contours
def detect_objects(frame, lower_bound, upper_bound, color_name, min_contour_size):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_mask = cv2.inRange(hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #put contours on original frame
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    
    largest_contour = None
    center = None
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_size:
            largest_contour = contour
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                center = (cx, cy)
                #draw at the ceneter of the color
                cv2.circle(frame, center, 7, (255, 255, 255), -1)
                break

    return frame, largest_contour, center

#haar cascade
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

# hsv range blue
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])
#purple
lower_dark_pink = np.array([150, 50, 50])
upper_dark_pink = np.array([180, 255, 255])

distance_to_face_blue = None
distance_to_face_dark_pink = None
exercise_count = 0
start_time = None
relaxing = False
relax_start_time = None
in_correct_posture = False
min_contour_size = 500  # değiştirerek test et
reset_timer = False 

while True:
    ret, frame = cap.read()

    frame = cv2.resize(frame, (640, 480))

    # detect blue object
    frame, largest_blue_contour, blue_center = detect_objects(frame.copy(), lower_blue, upper_blue, 'Blue', min_contour_size)


    frame, largest_dark_pink_contour, dark_pink_center = detect_objects(frame.copy(), lower_dark_pink, upper_dark_pink, 'Dark Pink', min_contour_size)

    # face
    frame, faces, face_center = detect_faces(frame.copy())

    # distance calc
    if blue_center  and face_center:
        distance_to_face_blue = np.sqrt((blue_center[0] - face_center[0])**2 + (blue_center[1] - face_center[1])**2)

    if dark_pink_center and face_center:
        distance_to_face_dark_pink = np.sqrt((dark_pink_center[0] - face_center[0])**2 + (dark_pink_center[1] - face_center[1])**2)

    # check distance
    if distance_to_face_blue and distance_to_face_dark_pink:
        if distance_to_face_blue < 160 and distance_to_face_dark_pink < 160:
            in_correct_posture = True
            if not relaxing:
                if start_time is None or reset_timer:
                    start_time = time.time()
                    reset_timer = False

                elapsed_time = time.time() - start_time

                
                countdown = 10 - int(elapsed_time)
                cv2.putText(frame, f'Exercise: {exercise_count + 1} - Countdown: {countdown}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                
                if elapsed_time >= 10:
                    exercise_count += 1
                    start_time = None
                    in_correct_posture = False  # reset for new ex
                    relaxing = True
                    relax_start_time = time.time()
        else:
            # Reset the timer if the posture is broken
            in_correct_posture = False
            reset_timer = True
            start_time = None
            relaxing = False
            cv2.putText(frame, f'Put yur hands on back of your head', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    
    if relaxing:
        relax_elapsed_time = time.time() - relax_start_time
        cv2.putText(frame, f'Relax for 5 seconds: {relax_elapsed_time:.2f}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if relax_elapsed_time >= 5:
            relaxing = False

            start_time = None 

            
    if exercise_count >= 3:
        break

    cv2.imshow('Frame with Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
