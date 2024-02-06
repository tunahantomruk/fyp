import cv2
import numpy as np

# Function to detect and draw contours around specified colors
def detect_objects(frame, lower_bound, upper_bound, color_name):
    # Convert the frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only specified colors
    color_mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Find contours in the binary image
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours around specified colors
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Find the largest contour
    largest_contour = None
    center = None
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the center of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx, cy)
            cv2.circle(frame, center, 7, (255, 255, 255), -1)
            print(f'{color_name} object detected at ({cx}, {cy})')

    return frame, largest_contour, center

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
        print(f'Face detected at ({face_center[0]}, {face_center[1]})')

    return frame, faces, face_center

# Arbitrary focal length value for demonstration purposes
focal_length = 1000

# Read the image from your webcam using DirectShow
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Define HSV ranges for blue and dark pink
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_dark_pink = np.array([150, 50, 50])
upper_dark_pink = np.array([180, 255, 255])

# Initialize variables outside the loop
distance_to_face_blue = None
distance_to_face_dark_pink = None

while True:
    ret, frame = cap.read()

    # Resize the frame to speed up processing
    frame = cv2.resize(frame, (640, 480))

    # Get the dominant colors from the frame
    # (You can replace this with the actual dominant colors from the ROIs if needed)
    dominant_color_blue = (120, 50, 50)  # Replace with actual dominant color for blue
    dominant_color_dark_pink = (160, 50, 50)  # Replace with actual dominant color for dark pink

    # Detect and draw contours around blue objects
    frame, largest_blue_contour, blue_center = detect_objects(frame.copy(), lower_blue, upper_blue, 'Blue')

    # Detect and draw contours around dark pink objects
    frame, largest_dark_pink_contour, dark_pink_center = detect_objects(frame.copy(), lower_dark_pink, upper_dark_pink, 'Dark Pink')

    # Detect and draw rectangles around faces
    frame, faces, face_center = detect_faces(frame.copy())

    # Print distances of colors to the face on the screen
    if blue_center is not None and face_center is not None:
        distance_to_face_blue = np.sqrt((blue_center[0] - face_center[0])**2 + (blue_center[1] - face_center[1])**2)
        print(f'Distance to Face (Blue): {distance_to_face_blue:.2f}')

    if dark_pink_center is not None and face_center is not None:
        distance_to_face_dark_pink = np.sqrt((dark_pink_center[0] - face_center[0])**2 + (dark_pink_center[1] - face_center[1])**2)
        print(f'Distance to Face (Dark Pink): {distance_to_face_dark_pink:.2f}')

    # Check if both colors have distances under 130 and display the message
    if distance_to_face_blue is not None and distance_to_face_dark_pink is not None:
        if distance_to_face_blue < 130 and distance_to_face_dark_pink < 130:
            cv2.putText(frame, 'Do the exercise!', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with blue and dark pink contours and faces
    cv2.imshow('Frame with Detection', frame)

    # Break the loop when the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()
