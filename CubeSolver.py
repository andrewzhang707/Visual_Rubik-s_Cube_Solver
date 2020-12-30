import sys
import cv2
import numpy as np

fWidth = 0.0
fHeight = 0.0

def findDominantColor(img, start, end):
    pixels = img[start[0]: end[0], start[1]: end[1]]

    n_colors = 6
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant

def testFindDominantColor():
    cap = cv2.VideoCapture(0)
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    start = (int(fWidth/2 -10), int(fHeight/2 - 10))
    end = (int(fWidth/2 + 10), int(fHeight/2 + 10))
    while True:
        ret, img = cap.read()
        cv2.rectangle(
            img,
            start,
            end,
            (0,255,0),
            2
        )
        dom = findDominantColor(img, start, end)
        print(dom)
        cv2.imshow("Dominant Color", img)
        if im.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

def TestReshape():
    cap = cv2.VideoCapture(0)
    while True:
        img = cap.read()
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        cv2.imshow(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
        

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
    cap.release()

#Parameters are each face of the cube as a 3x3 array
#Function returns a string in Cube Notation
def solver(yellow, white, blue, green, red, orange):
    print("wip")

def drawGrid(img, height, width, up, down, left, right):
    cv2.line(img, (int (width / 2 - height / 4), int (height / 4)),  (int (width / 2 + height / 4), int (height / 4)), (0, 255, 0))
    cv2.line(img, (int (width / 2 - height / 4), int (height / 4)),  (int (width / 2 - height / 4), int (3 * height / 4)), (0, 255, 0))
    cv2.line(img, (int (width / 2 + height / 4), int (3 * height / 4)),  (int (width / 2 + height / 4), int (height / 4)), (0, 255, 0))
    cv2.line(img, (int (width / 2 - height / 12), int (height / 4)),  (int (width / 2 - height / 12), int (3 * height / 4)), (0, 255, 0))
    cv2.line(img, (int (width / 2 + height / 12), int (3 * height / 4)),  (int (width / 2 + height / 12), int (height / 4)), (0, 255, 0))
    cv2.line(img, (int (width / 2 - height / 4), int (5 * height / 12)),  (int (width / 2 + height / 4), int (5 * height / 12)), (0, 255, 0))
    cv2.line(img, (int (width / 2 - height / 4), int (7 * height / 12)),  (int (width / 2 + height / 4), int (7 * height / 12)), (0, 255, 0))
    cv2.line(img, (int (width / 2 - height / 4), int (3 * height / 4)),  (int (width / 2 + height / 4), int (3 * height / 4)), (0, 255, 0))
    cv2.putText(img, up, (int (width / 2 - height / 12), int (height / 6)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(img, down, (int (width / 2 - height / 12), int (5 * height / 6)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(img, left, (int (width / 2 - 5 * height / 12), int (7 * height / 12)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(img, right, (int (width / 2 + 3 * height / 8), int (7 * height / 12)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)

def testDrawGrid():
    cap = cv2.VideoCapture(0)
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    while True:
        ret, frame = cap.read()
        drawGrid(frame,fHeight, fWidth, "yellow", "white", "red", "orange")
        cv2.imshow("Grid", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    