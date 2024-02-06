import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Face and Drawing modules
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Initialize MediaPipe Face Detection and Face Mesh models
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.3)
face_mesh = mp_face_mesh.FaceMesh()

# Open a connection to the camera (0 is usually the default camera)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while cap.isOpened():
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run face detection on the RGB frame
    results_detection = face_detection.process(rgb_frame)

    if results_detection.detections:
        for detection in results_detection.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            # Draw bounding box around the face
            cv2.rectangle(frame, bbox, (0, 255, 0), 2)

            # Run face mesh on the RGB frame
            results_mesh = face_mesh.process(rgb_frame)

            if results_mesh.multi_face_landmarks:
                for landmarks in results_mesh.multi_face_landmarks:
                    # Extract specific facial landmarks for eyes, nose, and mouth
                    left_eye = landmarks.landmark[33].x, landmarks.landmark[33].y
                    right_eye = landmarks.landmark[263].x, landmarks.landmark[263].y

                    # Calculate the angle between the eyes and the horizontal axis
                    angle_rad = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
                    angle_deg = math.degrees(angle_rad)

                    # Display the angle on the frame
                    cv2.putText(frame, f'Head Angle: {angle_deg:.2f} degrees', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Head Pose Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
