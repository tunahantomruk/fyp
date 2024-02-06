import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_detection

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  

with mp_face.FaceDetection(min_detection_confidence=0.2) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)

                nose = detection.location_data.relative_keypoints[0]
                left_eye = detection.location_data.relative_keypoints[1]
                right_eye = detection.location_data.relative_keypoints[2]

                angle_radians = abs(left_eye.x - right_eye.x) / abs(nose.y - (left_eye.y + right_eye.y) / 2)
                angle_degrees = round(angle_radians * (180.0 / 3.14), 2)

                cv2.putText(frame, f"Head Tilt Angle: {angle_degrees} degrees", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

                mp_drawing.draw_detection(frame, detection)

        cv2.imshow("Head Tilt Angle Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:  
            break

cap.release()
cv2.destroyAllWindows()
