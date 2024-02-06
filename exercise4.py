import mediapipe as mp
import cv2
import math
import time

font_scale = 1
text_color = (255, 255, 255)
line_thickness = 2

start_time = time.time()
exercise_done_time = None

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize MediaPipe Drawing module for annotations
mp_drawing = mp.solutions.drawing_utils

# Open a video capture (change 0 to another index if using a different camera)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose
    pose_results = pose.process(rgb_frame)

    # Draw pose landmarks on the frame
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get landmarks for wrists and head
        left_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        head_top = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
        right_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]

        # Calculate distances
        distance_right = math.sqrt((right_wrist.x - head_top.x)**2 + (right_wrist.y - head_top.y)**2)
        distance_left = math.sqrt((left_wrist.x - left_eye.x)**2 + (left_wrist.y - left_eye.y)**2)


        # Display distances on the frame
        text_color = (255, 255, 255)
        font_scale = 1
        line_thickness = 2

        if distance_left < 0.13:
            cv2.putText(frame, f'Left Hand on temporal side ', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Move Left Hand on temporal side', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        if distance_right < 0.13:
            cv2.putText(frame, f'Right Hand on back of head', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Move Right Hand to back of head', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        # Check if both conditions are met
        if distance_left < 0.13 and distance_right < 0.13:
            elapsed_time = time.time() - start_time
            cv2.putText(frame, f'HOLD', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

            if elapsed_time >= 5:
                cv2.putText(frame, f'1.Exercise Done!', (10, 140), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
                exercise_done_time = time.time()

                # Optionally break out of the loop or perform additional actions
                #break
        else:
            # Reset the start time if one of the conditions is not met
            start_time = time.time()
    # Display the frame
    cv2.imshow('Pose Estimation for New Exercise', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
