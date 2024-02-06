import cv2
import numpy as np

#3 tekrardan sonra aksi yöne dönmeli daire

# Load the pre-trained Haar cascade for face and nose
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
nose_cascade = cv2.CascadeClassifier('haar/nose.xml')  

# Open a connection to the webcam using cv2.CAP_DSHOW
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Initialize the angle variable
angle = 0

# Initialize variables for the progress bar and counter
start_time = None
progress_duration = 10  # seconds
progress_bar_height = 20
progress = 0
counter = 0

while True:
    # Read a frame from the webcam
    ret, frame = camera.read()

    # Create a copy of the frame for drawing
    img = frame.copy()

    # Convert the frame to grayscale for face and nose detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # If faces are found, detect nose in each face region
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        noses = nose_cascade.detectMultiScale(roi_gray)

        for (nx, ny, nw, nh) in noses:
            # Calculate the center of the detected nose
            nose_center = (x + nx + nw // 2, y + ny + nh // 2)

            # Calculate the distance from the center of the rotating circle to the nose
            circle_center = (frame.shape[1] // 2, frame.shape[0] // 2)
            circle_radius = 40

            # Rotate the circle around its center
            rotated_nose_center = (
                int(circle_center[0] + circle_radius * np.cos(np.radians(angle))),
                int(circle_center[1] + circle_radius * np.sin(np.radians(angle)))
            )

            # Check if the nose is inside the circle
            distance = np.sqrt((rotated_nose_center[0] - nose_center[0])**2 + (rotated_nose_center[1] - nose_center[1])**2)
            if distance < circle_radius:
                # If the nose is inside the circle, start the timer
                if start_time is None:
                    start_time = cv2.getTickCount()
                else:
                    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                    progress = min((elapsed_time / progress_duration) * 100, 100)

                    # Draw the progress bar
                    progress_bar_y = frame.shape[0] - progress_bar_height
                    cv2.rectangle(img, (0, progress_bar_y), (int(progress), frame.shape[0]), (0, 255, 0), -1)

                    # Check if the progress bar reaches 100%
                    if progress >= 100:
                        cv2.putText(img, "!ti did uoY !snoitalutargnoC", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        counter += 1
                        # You can add additional actions or reset the progress bar here
                        start_time = None
                        progress = 0

            # Draw the rotated circle and the detected nose on the frame
            cv2.circle(img, rotated_nose_center, circle_radius, (255, 255, 255), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(img, (x + nx, y + ny), (x + nx + nw, y + ny + nh), (0, 0, 255), 2)

    # Display the counter value on the frame
    counter_text = f"Trackbar filled: {counter} times"
    cv2.putText(img, counter_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Flip the frame horizontally for easier self-following
    img = cv2.flip(img, 1)

    # Display the frame
    cv2.imshow('Webcam', img)

    # Increment the angle for the next frame
    angle += 4  # You can adjust the rotation speed by changing this value

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(5)
    if key == 27:
        break

# Release the webcam and close all windows
camera.release()
cv2.destroyAllWindows()
