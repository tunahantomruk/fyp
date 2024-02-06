import cv2

# Load Haar cascade classifiers for left ear and right ear
left_ear_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_leftear.xml')
right_ear_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_rightear.xml')

leftTurn = 0
rightTurn = 0

# Set up video capture from a file
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Read frame from the video
    suc, frame = cap.read()
    if not suc:
        break

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect left ears
    left_ears = left_ear_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in left_ears:
        # Draw a red rectangle around the left ear
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # You've detected the left ear, increment leftTurn
        leftTurn += 1

    # Detect right ears
    right_ears = right_ear_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in right_ears:
        # Draw a blue rectangle around the right ear
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # You've detected the right ear, increment rightTurn
        rightTurn += 1

    # Print the counts
    print(f"Left Turns: {leftTurn}, Right Turns: {rightTurn}")

    # Display the frame
    cv2.imshow('Head Turning Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
