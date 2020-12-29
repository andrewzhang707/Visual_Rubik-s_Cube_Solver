import sys
import cv2

fWidth = 0.0
fHeight = 0.0

def recognizeFaces():
    scanning = True
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("video input not found")
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f'{fWidth} x {fHeight}')
    while scanning:
        ret, frame = cap.read()
        cv2.rectangle(frame, (0,0), (10,10), (0,255,0), 2)
        cv2.imshow("Cube", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#Parameters are each face of the cube as a 3x3 array
#Function returns a string in Cube Notation
def solver(yellow, white, blue, green, red, orange):
    print("wip")

recognizeFaces()