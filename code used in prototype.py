

import cv2
import numpy as np
import serial
import time
import dlib
from imutils import face_utils

# Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)
# ser = serial.Serial('/dev/ttyACM0',9600)
# Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/imagitronics/Desktop/shape_predictor_68_face_landmarks.dat")

# Constants for smoothing/filtering
SMOOTHING_FACTOR = 0.5  # Adjust this value to control the smoothing level

# Variables for nose position tracking
nose_position = "Center"  # Initial position
nose_position_history = []  # History of nose positions
history_length = 8  # Number of previous positions to consider for smoothing

def get_nose_position(nose_landmark, left_eye_landmark, right_eye_landmark, top_face_landmark, down_face_landmark):
    # Extract the x-coordinates of the landmark points
    nose_x = nose_landmark[0]
    left_eye_x = left_eye_landmark[0]
    right_eye_x = right_eye_landmark[0]
    upward_eye_x = top_face_landmark[0]
    downward_eye_x = down_face_landmark[0]

    # Compare the x-coordinates to determine the nose position
    if nose_x > left_eye_x and nose_x > right_eye_x:
        # ser.write(b'1')
        return "Left"  # Nose is positioned to the left of both eyes
    elif nose_x < left_eye_x and nose_x < right_eye_x:
        # ser.write(b'2')
        return "Right"  # Nose is positioned to the right of both eyes
    elif nose_x > upward_eye_x and nose_x > downward_eye_x:
        # ser.write(b'3')
        return "Upward"
    elif nose_x < upward_eye_x and nose_x < downward_eye_x :
        # ser.write(b'4')
        return "Downward"
    else:
        # ser.write(b'5')
        return "Center"  # Nose is positioned between the eyes




while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # Get the nose position
        new_nose_position = get_nose_position(landmarks[30], landmarks[39], landmarks[44], landmarks[51], landmarks[57])

        # Update nose position history
        nose_position_history.append(new_nose_position)
        if len(nose_position_history) > history_length:
            nose_position_history = nose_position_history[-history_length:]

        # Apply smoothing/filtering to the nose position
        smoothed_nose_position = max(set(nose_position_history), key=nose_position_history.count)
        nose_position = smoothed_nose_position

        # for n in range(0, 68):
        #     (x, y) = landmarks[n]
        #     cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

        # Display nose position on the frame
        # Display nose position on the frame
        cv2.putText(
            face_frame,
            "Nose: {}".format(nose_position),
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # Display the frame
        cv2.imshow("Result of detector", face_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
