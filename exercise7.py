import cv2
from math import sin, cos, radians

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face = cv2.CascadeClassifier("haar/haarcascade_frontalface_alt2.xml")

# Set up face detection parameters
settings = {
    'scaleFactor': 1.3,
    'minNeighbors': 6,
    'minSize': (50, 50),
    'flags': cv2.CASCADE_FIND_BIGGEST_OBJECT | cv2.CASCADE_DO_ROUGH_SEARCH #bu satır silinmeli mi
}

def rotate_image(image, angle):
    height, width, _ = image.shape
    center_of_image = (width / 2, height / 2)
    rot_mat = cv2.getRotationMatrix2D(center_of_image, angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    x = pos[0] - img.shape[1] * 0.4
    y = pos[1] - img.shape[0] * 0.4
    newx = x * cos(radians(angle)) + y * sin(radians(angle)) + img.shape[1] * 0.4
    newy = -x * sin(radians(angle)) + y * cos(radians(angle)) + img.shape[0] * 0.4
    return int(newx), int(newy), pos[2], pos[3]

while True:
    ret, img = camera.read()

    angle_found = False
    for angle in range(-60, 61, 5):
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)

        if detected is not None and len(detected) > 0:
            detected = [rotate_point(detected[-1], img, -angle)]
            angle_found = True
            break

    # Check if no faces are detected
    if not angle_found:
        # Handle the case where no faces are detected (e.g., display a message)
        print("No faces detected")
        continue  # Skip the rest of the loop and go to the next iteration

    # Make a copy as we don't want to draw on the original image:
    for x, y, w, h in detected[-1:]:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the current angle on the video stream:
    cv2.putText(img, f'Angle: {angle + 10}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('facedetect', img)

    # Check for the escape key (27 is the ASCII code for Esc)
    key = cv2.waitKey(5)
    if key == 27:
        break

# Release the camera and destroy OpenCV windows
camera.release()
cv2.destroyAllWindows()
