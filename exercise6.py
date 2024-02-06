import cv2
from math import sin, cos, radians
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face = cv2.CascadeClassifier("haar/haarcascade_mcs_leftear.xml")

# kulak ile yap(haar cascade'i) , optical flow kullanılabilir.
#optical flow ekle laf olsun diye dense ekle hareket yönünü tespit et 

#  eksi açılardan kurtulmak için optical flow ile kafanın hangi yöne eğildiğine bakılabilir
#ya da eksi yazdırma bu kadar basit açıların en son mutlağını al

# parametre olarak kullanmak iiçn **settings olarak kullan bkz dictionary unpacking

settings = {
    'scaleFactor': 1.3,
    'minNeighbors': 3,
    'minSize': (50, 50),
    'flags': cv2.CASCADE_FIND_BIGGEST_OBJECT | cv2.CASCADE_DO_ROUGH_SEARCH
}

def rotate_image(image, angle):
    if angle == 0:
        return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0:
        return pos
    x = pos[0] - img.shape[1] * 0.4
    y = pos[1] - img.shape[0] * 0.4
    newx = x * cos(radians(angle)) + y * sin(radians(angle)) + img.shape[1] * 0.4
    newy = -x * sin(radians(angle)) + y * cos(radians(angle)) + img.shape[0] * 0.4
    return int(newx), int(newy), pos[2], pos[3]

while True:
    ret, img = camera.read()

    angle_found = False
    for angle in range(-60, 61,5):
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        if len(detected):
            detected = [rotate_point(detected[-1], img, -angle)]
            angle_found = True
            break

    # Make a copy as we don't want to draw on the original image:
    for x, y, w, h in detected[-1:]:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the current angle on the video stream:
    if angle_found:
        cv2.putText(img, f'Angle: {angle}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('facedetect', img)

    key = cv2.waitKey(5)
    if key == 27:
        break

cv2.destroyWindow("facedetect")
