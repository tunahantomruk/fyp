import cv2
import numpy as np

# Function to get the dominant color
def get_dominant_color(image):
    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a list of pixels
    pixels = image_rgb.reshape((-1, 3))

    # Calculate the dominant color using k-means clustering
    k = 3  # Number of clusters for blue, red, and yellow
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
    _, labels, centers = cv2.kmeans(np.float32(pixels), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert the dominant colors back to integers
    dominant_colors = np.uint8(centers)

    return dominant_colors

# Function to detect and draw contours around blue objects
def detect_blue_objects(frame):
    # Convert the frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours in the binary image
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours around blue objects
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Find the largest contour
    largest_contour = None
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the center of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)

    return frame, largest_contour

# Function to detect and draw a rectangle around faces using Haar cascades
def detect_faces(frame):
    # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # Initialize face_center variable
    face_center = None

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Calculate the center of the first face (assuming there is at least one face)
        face_center = (int(x + w / 2), int(y + h / 2))
        cv2.circle(frame, face_center, 7, (255, 255, 255), -1)

    return frame, faces, face_center

# Arbitrary focal length value for demonstration purposes
focal_length = 1000

# Read the image from your webcam using DirectShow
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)



while True:
    ret, frame = cap.read()

    # Resize the frame to speed up processing
    frame = cv2.resize(frame, (640, 480))

    # Define a region of interest (ROI)
    roi = frame[100:400, 200:500]

    # Get the dominant color from the ROI
    dominant_color = get_dominant_color(roi)

    # Detect and draw contours around blue objects
    frame_with_blue_contours, largest_blue_contour = detect_blue_objects(frame.copy())

    # Detect and draw rectangles around faces
    frame_with_faces, faces, face_center = detect_faces(frame_with_blue_contours)

    # Display the frame with blue contours and faces
    #cv2.imshow('Frame with Detection', frame_with_faces)

    # Calculate distance estimation
    if largest_blue_contour is not None and face_center is not None:
        # Calculate the center of the largest blue contour
        M_blue = cv2.moments(largest_blue_contour)
        if M_blue["m00"] != 0:
            cx_blue = int(M_blue["m10"] / M_blue["m00"])
            cy_blue = int(M_blue["m01"] / M_blue["m00"])

            # Calculate the distance based on the Euclidean distance between centers
            distance = np.sqrt((cx_blue - face_center[0])**2 + (cy_blue - face_center[1])**2)

            # Display the estimated distance
            print('Estimated Distance:', distance)

            # Exercise message parameters
            exercise_message = "Do the exercise"
            exercise_position = (100, 100)  # Set the desired position
            exercise_font = cv2.FONT_HERSHEY_SIMPLEX
            exercise_font_scale = 1
            exercise_font_color = (0, 0, 255)  # Red color
            exercise_font_thickness = 2

            # Display "Do the exercise" message if the distance is under 150
            if distance < 120:
                cv2.putText(frame_with_faces, exercise_message, exercise_position, exercise_font, exercise_font_scale, exercise_font_color, exercise_font_thickness)
                #print("OKKOKKKKKKKKKKK!!")
            cv2.imshow('Frame with Detection', frame_with_faces)
    # Break the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()
