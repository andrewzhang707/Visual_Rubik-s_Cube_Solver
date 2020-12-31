import sys
import cv2
import numpy as np
import enum

class Colors(enum.Enum):
    Bad = 0
    Blue = 1
    Red = 2
    Green = 3
    Orange = 4
    White = 5
    Yellow = 6

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
fWidth = 0.0
fHeight = 0.0
PICTURESdir = "PICTURES/"

def WhiteBalanceTest():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        white = frame.copy()
        white = white_balance(white)
        cv2.imshow("normal", frame)
        cv2.imshow("white balance", white)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def convertBGRToHSV(bgrColor):
    bgrColor = (bgrColor[0]/255, bgrColor[1]/255, bgrColor[2]/255)
    v = max(bgrColor)
    s = (v - min(bgrColor))/v if v != 0 else 0
    h = 0
    if (v - min(bgrColor) == 0):
        h = 0
    elif v == bgrColor[2]:
        h = 60*(bgrColor[1]-bgrColor[0])/(v - min(bgrColor))
    elif v == bgrColor[1]:
        h = 120 + 60*(bgrColor[0] - bgrColor[2])/(v - min(bgrColor))
    elif v == bgrColor[0]:
        h = 240+60*(bgrColor[2]-bgrColor[1])/(v-min(bgrColor))
    if(0> h):
        h = 0
    if(h> 360):
        print(f"BAD H VALUE: {h}")
    
    return (h,s,v)

def getBlockColorType(bgrColor):
    yellow = (45, 90)
    blue = (175, 250)
    green = (100, 160)
    redLow = (0, 6)
    redHigh = (330, 359)
    orange = (7, 40)
    whiteS = (0, 0.3)
    hsv = convertBGRToHSV(bgrColor)
    print(hsv)
    if (hsv[1] >= whiteS[0] and hsv[1] <= whiteS[1]):
        return Colors.White
    if (hsv[0] >= yellow[0] and hsv[0] <= yellow[1]):
        return Colors.Yellow
    if (hsv[0] >= blue[0] and hsv[0] <= blue[1]):
        return Colors.Blue
    if (hsv[0] >= green[0] and hsv[0] <= green[1]):
        return Colors.Green
    if ((hsv[0] >= redHigh[0] and hsv[0] <= redHigh[1]) or
        (hsv[0] >= redLow[0] and hsv[0] <= redLow[1])):
        return Colors.Red
    if(hsv[0] >= orange[0] and hsv[0] <= orange[1]):
        return Colors.Orange
    return Colors.Bad

def testColorIdTest():
    cap = cv2.VideoCapture(0)
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    start = (int(fWidth/2 -10), int(fHeight/2 - 10))
    end = (int(fWidth/2 + 10), int(fHeight/2 + 10))
    while True:
        ret, img = cap.read()
        img = white_balance(img)
        dom = findDominantColor(img, start, end)
        color = getBlockColorType(dom)
        text = {
            Colors.White : "White",
            Colors.Yellow :"Yellow",
            Colors.Blue : "Blue",
            Colors.Green : "Green",
            Colors.Orange : "Orange",
            Colors.Red : "Red",
            Colors.Bad : "Super Bad"
        }

        cv2.putText(
            img, 
            f"Target color is {text[color]}", 
            (0, int (fHeight / 10)), 
            cv2.FONT_HERSHEY_COMPLEX, 
            1, 
            GREEN, 
            3
        )
        cv2.rectangle(img, start, end, dom, 2)
        cv2.imshow("Actual Color", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

def findDominantColor(img, start, end):
    pixels = img[start[1]: end[1], start[0]: end[0]]
    reshaped = np.reshape(pixels, (-1,3))
    unique, counts = np.unique(reshaped, axis=0, return_counts=True)
    dominant = unique[np.argmax(counts)]
    # these need to be utf-8 int type, otherwise openCV's rectangle 
    # and related functions will not recognize it as acceptable parameter
    return (int(dominant[0]), int(dominant[1]), int(dominant[2]))

def testFindDominantColor():
    cap = cv2.VideoCapture(0)
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    start = (int(fWidth/2 -10), int(fHeight/2 - 10))
    end = (int(fWidth/2 + 10), int(fHeight/2 + 10))
    while True:
        ret, img = cap.read()
        dom = findDominantColor(img, start, end)
        imgCopy = img.copy()
        cv2.rectangle(
            img,
            start,
            end,
            (0,255,0),
            2
        )
        
        cv2.rectangle(imgCopy, start, end, dom, 2)
        cv2.imshow("Dominant Color", img)
        cv2.imshow("Actual Color", imgCopy)
        if cv2.waitKey(1) & 0xFF == ord('q'):
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
        

def captureFace(cap, fHeight, fWidth, color, up, down, left, right):
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, "Please show " + color + " face", (0, int (fHeight / 10)), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 3)
        drawGrid(frame, fHeight, fWidth, up, down, left, right)
        cv2.imshow("Cube", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(PICTURESdir + color + "-file.bmp", frame)
            break

def recognizeFaces():
    scanning = True
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("video input not found")
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    captureFace(cap, fHeight, fWidth, "green", "yellow", "white", "red", "orange")
    captureFace(cap, fHeight, fWidth, "red", "yellow", "white", "blue", "green")
    captureFace(cap, fHeight, fWidth, "blue", "yellow", "white", "orange", "red")
    captureFace(cap, fHeight, fWidth, "orange", "yellow", "white", "green", "blue")
    captureFace(cap, fHeight, fWidth, "yellow", "green", "blue", "orange", "red")
    captureFace(cap, fHeight, fWidth, "white", "blue", "green", "orange", "red")
    cap.release()

#Parameters are each face of the cube as a 3x3 array
#Function returns a string in Cube Notation
def solver(yellow, white, blue, green, red, orange):
    print("wip")

def drawGrid(img, height, width, up, down, left, right):
    leftX = int (width / 2 - height / 4)
    upperY = int (height / 4)
    rightX = int (width / 2 + height / 4)
    lowerY = int (3 * height / 4)
    firstSplitX = int (width / 2 - height / 12)
    secondSplitX = int (width / 2 + height / 12)
    firstSplitY = int (5 * height / 12)
    secondSplitY = int (7 * height / 12)
    cv2.line(img, (leftX, upperY),  (rightX, upperY), GREEN)
    cv2.line(img, (leftX, upperY),  (leftX, lowerY), GREEN)
    cv2.line(img, (rightX, lowerY),  (rightX, upperY), GREEN)
    cv2.line(img, (firstSplitX, upperY),  (firstSplitX, lowerY), GREEN)
    cv2.line(img, (secondSplitX, lowerY),  (secondSplitX, upperY), GREEN)
    cv2.line(img, (leftX, firstSplitY),  (rightX, firstSplitY), GREEN)
    cv2.line(img, (leftX, secondSplitY),  (rightX, secondSplitY), GREEN)
    cv2.line(img, (leftX, lowerY),  (rightX, lowerY), GREEN)
    cv2.putText(img, up, (firstSplitX, int (height / 6)), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 3)
    cv2.putText(img, down, (firstSplitX, int (5 * height / 6)), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 3)
    cv2.putText(img, left, (int (width / 2 - 5 * height / 12), secondSplitY), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 3)
    cv2.putText(img, right, (int (width / 2 + 9 * height / 32), secondSplitY), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 3)

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