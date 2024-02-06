import mediapipe as mp
import cv2
import math
import time

font_scale = 1
text_color = (255, 255, 255)
line_thickness = 2

exercise_start_time = time.time()
rest_start_time = time.time()
exercise_done_time = None
relaxing = False
reset_timer = False
exercise_count = 0

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_results = pose.process(rgb_frame)

    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        left_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        head_top = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
        right_eye = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]

        distance_left = math.sqrt((left_wrist.x - head_top.x)**2 + (left_wrist.y - head_top.y)**2)
        distance_right = math.sqrt((right_wrist.x - right_eye.x)**2 + (right_wrist.y - right_eye.y)**2)

        text_color = (255, 255, 255)
        font_scale = 1
        line_thickness = 2

        elapsed_time = time.time() - exercise_start_time
        exercise_countdown = max(0, 10 - int(elapsed_time))
        cv2.putText(frame, f'Exercise: {exercise_count + 1} - Countdown: {exercise_countdown}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness)

        if distance_left < 0.13:
            cv2.putText(frame, f'Left Hand Behind Head', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Move Left Hand Behind Head', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        if distance_right < 0.13:
            cv2.putText(frame, f'Right Hand on Side of Forehead', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)
        else:
            cv2.putText(frame, f'Move Right Hand to Side of Forehead', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness, cv2.LINE_AA)

        if distance_left < 0.13 and distance_right < 0.13 and not relaxing:
            cv2.putText(frame, f'HOLD', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness)

            if elapsed_time >= 10:
                cv2.putText(frame, f'Exercise Done!', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness)
                exercise_done_time = time.time()

                exercise_count += 1
                exercise_start_time = time.time()
                reset_timer = True
                relaxing = True
                rest_start_time = time.time()

                if exercise_count >= 3:
                    break
        else:
            exercise_start_time = time.time()

        if relaxing:
            rest_elapsed_time = time.time() - rest_start_time
            rest_countdown = max(0, 5 - int(rest_elapsed_time))
            cv2.putText(frame, f'Rest Countdown: {rest_countdown}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, line_thickness)

            if rest_elapsed_time >= 5:
                relaxing = False
                rest_start_time = time.time()

    cv2.imshow('Pose Estimation for New Exercise', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
