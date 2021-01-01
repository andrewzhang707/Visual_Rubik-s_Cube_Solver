import sys
import cv2
import numpy as np
import enum

class Colors(enum.IntEnum):
    Bad = 0
    Blue = 1
    Orange = 2
    Green = 3
    Red = 4
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

def findColors(img, width, height):
    rows, cols = (3, 3) 
    colorsArr = []
    for i in range(cols): 
        col = []
        startY = int ( 7 * height / 24 + i * height / 6)
        endY = int (startY + height / 12)
        for j in range(rows):
            startX = int (width / 2 - 5 * height / 24 + j * height / 6)
            endX = int (startX + height / 12)
            col.append(findDominantColor(img, (startX, startY), (endX, endY)))
        colorsArr.append(col)
    return colorsArr

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
def convertToColorEnum(faceColor):
    face = []
    for row in faceColor:
        faceRow = []
        for bgr in row:
            faceRow.append(getBlockColorType(bgr))
        face.append(faceRow)
    return face

def captureFace(cap, fHeight, fWidth, color, up, down, left, right):
    while True:
        ret, frame = cap.read()
        img = frame.copy()
        cv2.putText(frame, "Please show the " + color + " face and press Q when aligned correctly", (0, int (fHeight / 10)), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 3)
        drawGrid(frame, fHeight, fWidth, up, down, left, right)
        cv2.imshow("Cube", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            dominantColors = findColors(img,fWidth, fHeight)
            return convertToColorEnum(dominantColors)

def recognizeFaces():
    scanning = True
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("video input not found")
    fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    greenFace = captureFace(cap, fHeight, fWidth, "green", "yellow", "white", "red", "orange")
    redFace = captureFace(cap, fHeight, fWidth, "red", "yellow", "white", "blue", "green")
    blueFace = captureFace(cap, fHeight, fWidth, "blue", "yellow", "white", "orange", "red")
    orangeFace = captureFace(cap, fHeight, fWidth, "orange", "yellow", "white", "green", "blue")
    yellowFace = captureFace(cap, fHeight, fWidth, "yellow", "green", "blue", "orange", "red")
    whiteFace = captureFace(cap, fHeight, fWidth, "white", "blue", "green", "orange", "red")
    cap.release()
    return (greenFace, redFace, blueFace, orangeFace, yellowFace, whiteFace)

def testCaptureFace():
    cap = cv2.VideoCapture(0)
    while True:
        fWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        fHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        greenFace = captureFace(cap, fHeight, fWidth, "green", "yellow", "white", "red", "orange")
        print(f"array len = {len(greenFace)}")
        print(greenFace)

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
class Face:
    def __init__(self, face_colors):
        self.colors = face_colors[:][:]
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
    def turn_right(self):
        temp = [None]*3
        top_orientations = [2,1,0,2,2,2,0,1,2,0,0,0]
        bottom_orientations = [0,1,2,2,2,2,2,1,0,0,0,0]
        bottom_color = self.colors[1][1]
        if(bottom_color%2 == 0):
            bottom_color = bottom_color + (2*pow((-1),(bottom_color/2+1)))
        row_start = 3 * (bottom_color - 1)
        col_start = (3*bottom_color) % 12
        temp[0] = self.bottom.colors[bottom_orientations[row_start]][bottom_orientations[col_start]]
        temp[1] = self.bottom.colors[bottom_orientations[row_start+1]][bottom_orientations[col_start+1]]
        temp[2] = self.bottom.colors[bottom_orientations[row_start+2]][bottom_orientations[col_start+2]]
        self.bottom.colors[bottom_orientations[row_start]][bottom_orientations[col_start]] = self.right.right.colors[2][0]
        self.bottom.colors[bottom_orientations[row_start+1]][bottom_orientations[col_start+1]] = self.right.right.colors[1][0]
        self.bottom.colors[bottom_orientations[row_start+2]][bottom_orientations[col_start+2]] = self.right.right.colors[0][0]
        row_start = 3 * (self.colors[1][1] - 1)
        col_start = (3*self.colors[1][1]) % 12
        self.right.right.colors[0][0] = self.top.colors[top_orientations[row_start]][top_orientations[col_start]]
        self.right.right.colors[1][0] = self.top.colors[top_orientations[row_start+1]][top_orientations[col_start+1]]
        self.right.right.colors[2][0] = self.top.colors[top_orientations[col_start+2]][top_orientations[col_start+2]]
        self.top.colors[top_orientations[row_start]][top_orientations[col_start]] =self.colors[0][2]
        self.top.colors[top_orientations[row_start+1]][top_orientations[col_start+1]] =self.colors[1][2]
        self.top.colors[top_orientations[row_start+2]][top_orientations[col_start+2]] =self.colors[2][2]
        self.colors[0][2]=temp[0]
        self.colors[1][2]=temp[1]
        self.colors[2][2]=temp[2]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = self.right.colors[2][0]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.right.colors[3-j][i]
                    temp_index += 1
                self.right.colors[3-j][i]=self.right.colors[i+add_array[i]][3-j] 
        self.right.colors[0][1] = temp[0]
        self.right.colors[0][2] = temp[1]
        self.right.colors[1][2] = temp[2]
        self.right.colors[0][0] = stemp  
    def turn_left(self):
        temp = [None] * 3
        top_orientations = [0,1,2,0,0,0,2,1,0,2,2,2]
        bottom_orientations = [2,1,0,2,2,2,0,1,2,0,0,0]
        row_start = 3 * (self.colors[1][1] - 1)
        col_start = (9 + 3 * (self.colors[1][1] - 1)) % 12
        temp[0] = self.bottom.colors[bottom_orientations[row_start]][bottom_orientations[col_start]]
        temp[1] = self.bottom.colors[bottom_orientations[row_start + 1]][bottom_orientations[col_start + 1]]
        temp[2] = self.bottom.colors[bottom_orientations[row_start + 2]][bottom_orientations[col_start + 2]]
        self.bottom.colors[bottom_orientations[row_start]][bottom_orientations[col_start]] = self.colors[0][0]
        self.bottom.colors[bottom_orientations[row_start + 1]][bottom_orientations[col_start + 1]] = self.colors[1][0]
        self.bottom.colors[bottom_orientations[row_start + 2]][bottom_orientations[col_start + 2]] = self.colors[2][0]
        row_start = 3 * (self.colors[1][1] - 1)
        col_start = (3 * self.colors[1][1]) % 12
        self.colors[0][0] = self.top.colors[top_orientations[row_start]][top_orientations[col_start]]
        self.colors[1][0] = self.top.colors[top_orientations[row_start+1]][top_orientations[col_start+1]]
        self.colors[2][0] = self.top.colors[top_orientations[row_start+2]][top_orientations[col_start+2]]
        self.top.colors[top_orientations[row_start]][top_orientations[col_start]] = self.left.left.colors[0][2]
        self.top.colors[top_orientations[row_start+1]][top_orientations[col_start+1]] = self.left.left.colors[1][2]
        self.top.colors[top_orientations[row_start+2]][top_orientations[col_start+2]] = self.left.left.colors[2][2]
        self.left.left.colors[0][2] = temp[0]
        self.left.left.colors[1][2] = temp[1]
        self.left.left.colors[2][2] = temp[2]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = self.left.colors[2][0]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.left.colors[3-j][i]
                    temp_index += 1
                self.left.colors[3-j][i]=self.left.colors[i+add_array[i]][3-j] 
        self.left.colors[0][1] = temp[0]
        self.left.colors[0][2] = temp[1]
        self.left.colors[1][2] = temp[2]
        self.left.colors[0][0] = stemp
    def turn_upper(self):
        temp = [None] *3
        temp[0] = self.colors[0][0]
        temp[1] = self.colors[0][1]
        temp[2] = self.colors[0][2]
        self.colors[0][0] = self.right.colors[0][0]
        self.colors[0][1] = self.right.colors[0][1]
        self.colors[0][2]  = self.right.colors[0][2] 
        self.right.colors[0][0] = self.right.right.colors[0][0]
        self.right.colors[0][1] = self.right.right.colors[0][1]
        self.right.colors[0][2] = self.right.right.colors[0][2] 
        self.right.right.colors[0][0] = self.left.colors[0][0]
        self.right.right.colors[0][1] = self.left.colors[0][1]
        self.right.right.colors[0][2]  = self.left.colors[0][2] 
        self.left.colors[0][0]=temp[0]
        self.left.colors[0][1]=temp[1]
        self.left.colors[0][2] =temp[2]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = self.top.colors[2][0]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.top.colors[3-j][i]
                    temp_index += 1
                self.top.colors[3-j][i]=self.top.colors[i+add_array[i]][3-j] 
        self.top.colors[0][1] = temp[0]
        self.top.colors[0][2] = temp[1]
        self.top.colors[1][2] = temp[2]
        self.top.colors[0][0] = stemp
    def turn_lower(self): 
        temp = [None] * 3
        temp[0] = self.colors[2][0]
        temp[1] = self.colors[2][1]
        temp[2] = self.colors[2][2]
        self.colors[2][0] = self.left.colors[2][0]
        self.colors[2][1] = self.left.colors[2][1]
        self.colors[2][2]  = self.left.colors[2][2] 
        self.left.colors[2][0] = self.right.right.colors[2][0]
        self.left.colors[2][1] = self.right.right.colors[2][1]
        self.left.colors[2][2]  = self.right.right.colors[2][2] 
        self.right.right.colors[2][0] = self.right.colors[2][0]
        self.right.right.colors[2][1] = self.right.colors[2][1]
        self.right.right.colors[2][2]  = self.right.colors[2][2] 
        self.right.colors[2][0]=temp[0]
        self.right.colors[2][1]=temp[1]
        self.right.colors[2][2] =temp[2]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = self.bottom.colors[2][0]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.bottom.colors[3-j][i]
                    temp_index += 1
                self.bottom.colors[3-j][i]=self.bottom.colors[i+add_array[i]][3-j] 
        self.bottom.colors[0][1] = temp[0]
        self.bottom.colors[0][2] = temp[1]
        self.bottom.colors[1][2] = temp[2]
        self.bottom.colors[0][0] = stemp

def createCube(bColor, rColor, gColor, oColor, wColor, yColor):
    blue = Face(bColor) 
    red = Face(rColor)
    orange = Face(oColor)
    green = Face(gColor)
    white = Face(wColor)
    yellow = Face(yColor)

    yellow.left = orange
    yellow.right = red
    yellow.top = green
    yellow.bottom = blue

    blue.left = orange
    blue.right = red
    blue.top = yellow
    blue.bottom = white

    red.left = blue
    red.right = green
    red.top = yellow
    red.bottom = white

    green.left = red
    green.right = orange
    green.top = yellow
    green.bottom = white

    orange.left = green
    orange.right = blue
    orange.top = yellow
    orange.bottom = white

    white.left = orange
    white.right = red
    white.top = blue
    white.bottom = green

    return(blue, red, green, orange, white, yellow)


def fillTestFace(color):
    face = []
    for i in range(3):
        row = []
        for ii in range(3):
            row.append(color)
        face.append(row)
    return face

# input is a tuple of 6 faces, each face is a 3x3 color matrix
#   Order of tuple is blue, red, green, orange, white and yellow
# output is same format as input, but with expected colors
def TurnLogicUnitTest():
    bColor = fillTestFace(Colors.Blue)
    rColor = fillTestFace(Colors.Red)
    gColor = fillTestFace(Colors.Green)
    oColor = fillTestFace(Colors.Orange)
    wColor = fillTestFace(Colors.White)
    yColor = fillTestFace(Colors.Yellow)

    (blue, red, green, orange, white, yellow) = createCube(bColor, rColor, gColor, oColor, wColor, yColor)

    blue.turn_lower()

    print("blue: ")
    print(blue.colors)
    print("")

    print("red: ")
    print(red.colors)
    print("")

    print("green: ")
    print(green.colors)
    print("")

    print("orange: ")
    print(orange.colors)
    print("")

    print("white: ")
    print(white.colors)
    print("")

    print("yellow: ")
    print(yellow.colors)
    print("")
    
TurnLogicUnitTest()