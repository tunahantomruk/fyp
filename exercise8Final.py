import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier('haar/nose.xml')

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

angle = 0
angle_direction = 1  

start_time = None
progress_duration = 10  
progress_bar_height = 20
progress = 0
counter = 0

total_rep = 0

while True:
    ret, frame = camera.read()
    
    img = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        #roi yden y+hye xten x+wye kadar olan yüzey
        roi_gray = gray[y:y + h, x:x + w]
        noses = nose_cascade.detectMultiScale(roi_gray)

        for (nx, ny, nw, nh) in noses:
            #add x and y from face to make it relative to the entire frame
            nose_center = (x + nx + nw // 2, y + ny + nh // 2)

           
            circle_center = (frame.shape[1] // 2, frame.shape[0] // 2)
            circle_radius = 40

            # rotate the circle
            rotated_nose_center = (
                #x
                int(circle_center[0] + circle_radius * np.cos(np.radians(angle))),
                #y
                int(circle_center[1] + circle_radius * np.sin(np.radians(angle)))
            )

            # check nose is inside circle
            distance = np.sqrt((rotated_nose_center[0] - nose_center[0]) ** 2 + (rotated_nose_center[1] - nose_center[1]) ** 2)
            if distance < circle_radius:
                if start_time is None:
                    start_time = cv2.getTickCount()
                else:
                    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                    progress = min((elapsed_time / progress_duration) * 100, 100)

                    progress_bar_y = frame.shape[0] - progress_bar_height
                    #cv2.rectangle(img,topleft, bottomrigt
                    cv2.rectangle(img, (0, progress_bar_y), (int(progress), frame.shape[0]), (0, 255, 0), -1)

                    if progress >= 100:
                        counter += 1
                        total_rep += 1
                        if counter >= 3:
                            angle_direction *= -1  
                            counter = 0  

                        start_time = None
                        progress = 0

            cv2.circle(img, rotated_nose_center, circle_radius, (255, 255, 255), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(img, (x + nx, y + ny), (x + nx + nw, y + ny + nh), (0, 0, 255), 2)

    

    
    img = cv2.flip(img, 1)
    counter_text = f"Trackbar filled: {counter} times"
    cv2.putText(img, counter_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.putText(img, "Follow the circle with your nose", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (200, 0, 0), 2)

    cv2.imshow('Webcam', img)

    #speed
    angle += (4 * angle_direction) 
    if total_rep >= 6:
        break
    key = cv2.waitKey(5)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
