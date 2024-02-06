import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

# Function to calculate head angle
def calculate_head_angle(nose_landmark):
    # Extract nose coordinates
    x, y = nose_landmark.x, nose_landmark.y

    # Calculate the angle using arctangent
    angle = math.degrees(math.atan2(x, y))

    return angle

# Your video capture code goes here
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect face landmarks
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)
            # Get nose landmark
            nose_landmark = detection.location_data.relative_keypoints[0]

            # Calculate head angle
            angle = calculate_head_angle(nose_landmark)
            print(f"Heading angle: {angle} degrees")

    cv2.imshow("Head Angle Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
