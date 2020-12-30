import cv2
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
    