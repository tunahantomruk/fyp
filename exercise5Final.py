import cv2

left_ear_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_leftear.xml')
right_ear_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_rightear.xml')

leftTurn = 0
rightTurn = 0
rightRep = 0
leftRep = 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    left_ears = left_ear_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in left_ears:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        leftTurn += 1

    right_ears = right_ear_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in right_ears:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        rightTurn += 1

    if rightTurn % 50 == 0 and rightTurn!=0:
        rightRep+=1
        rightTurn = 0 
    if leftTurn % 50 == 0 and leftTurn !=0:
        leftRep+=1
        leftTurn = 0

    cv2.putText(frame, f"Left Turns: {rightRep}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Right Turns: {leftRep}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow('Head Turning Detection', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
