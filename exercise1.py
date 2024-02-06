import mediapipe as mp
import cv2
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

#çizim için
mp_drawing = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe 
    pose_results = pose.process(rgb_frame)

    # landmarkları çiz
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # keypointleri tanımla
        left_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
        right_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]

        
        distance_left = math.sqrt((left_wrist.x - left_eye.x)**2 + (left_wrist.y - left_eye.y)**2)
        distance_right = math.sqrt((right_wrist.x - right_eye.x)**2 + (right_wrist.y - right_eye.y)**2)

        
        text_color = (255, 255, 255)
        font_scale = 1
        line_thickness = 2
        # uzaklığı 0.13 yap
        if distance_left < 0.15:
            cv2.putText(frame, f'Distance Left: {distance_left:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Lower Your Left Hand', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        if distance_right < 0.15:
            cv2.putText(frame, f'Distance Right: {distance_right:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Lower Your Right Hand', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        #doğru formn
        if  distance_left < 0.15 and  distance_right < 0.15:
            cv2.putText(frame, 'Push Your Hands and Head in Opposite Ways!', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)



    cv2.imshow('Pose Estimation with Distances', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
