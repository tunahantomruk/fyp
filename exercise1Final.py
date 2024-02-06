import mediapipe as mp
import cv2
import math
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()



cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


exercise_count = 0
start_time = None
in_correct_posture = False
relaxing = False
relax_start_time = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # frame i pose ile process et
    pose_results = pose.process(rgb_frame)

    # if landmark detected landmark çiz
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    
        left_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
        right_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]

        distance_left = math.sqrt((left_wrist.x - left_eye.x)**2 + (left_wrist.y - left_eye.y)**2)
        distance_right = math.sqrt((right_wrist.x - right_eye.x)**2 + (right_wrist.y - right_eye.y)**2)

        text_color = (255, 255, 255)
        font_scale = 1
        line_thickness = 2

        if distance_left < 0.15 and distance_right < 0.15:
            in_correct_posture = True
            cv2.putText(frame, f'Distance Left: {distance_left:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
            cv2.putText(frame, f'Distance Right: {distance_right:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            in_correct_posture = False
            start_time = None  # Reset timer when the pooture is not true, 
            cv2.putText(frame, f'Lower Your Hands', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        # Check form
        if not relaxing:
            if in_correct_posture:
                if start_time is None:
                    start_time = time.time()

                elapsed_time = time.time() - start_time

                
                countdown = 10 - int(elapsed_time)
                cv2.putText(frame, f'Exercise: {exercise_count + 1} - Countdown: {countdown}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

                # Check if 10 seconds have passed
                if elapsed_time >= 10:
                    start_time = None
                    in_correct_posture = False
                    relaxing = True
                    relax_start_time = time.time()

    else:
        #poz doğeu değilse reset time
        in_correct_posture = False
        start_time = None 

    
    if relaxing:
        # 5                =    şuan     -    egzersizin bittiği zaman
        relax_elapsed_time = time.time() - relax_start_time
        cv2.putText(frame, 'Relax for 5 seconds', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        if relax_elapsed_time >= 5:
            relaxing = False
            exercise_count += 1

            
            if exercise_count >= 3:
                break

    
    cv2.imshow('Pose Estimation with Distances', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
