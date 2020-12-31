import sys
import cv2
import numpy as np
import enum

class Colors(enum.Enum):
    Yellow = 0
    Blue = 1
    Orange = 2
    Green = 3
    Red = 4
    White = 5

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
fWidth = 0.0
fHeight = 0.0
PICTURESdir = "PICTURES/"
def convertBGRToHSV(bgrColor):
    bgrColor = (bgrColor[0]/255, bgrColor[1]/255, bgrColor[2]/255)
    v = max(bgrColor)
    s = (v - min(bgrColor))/v if v != 0 else 0
    h = 0
    if v == bgrColor[2]:
        h = 60*(bgrColor[1]-bgrColor[0])/(v - min(bgrColor))
    elif v == bgrColor[1]:
        h = 120 + 60*(bgrColor[0] - bgrColor[2])/(v - min(bgrColor))
    elif v == bgrColor[0]:
        h = 240+60*(bgrColor[2]-bgrColor[1])/(v-min(bgrColor))
    if(h> 360 or h< 0):
        print(f"BAD H VALUE: {h}")
    return (h,s,v)

def getBlockColorType(bgrColor):
    yellow = (45, 75)
    blue = (175, 250)
    green = (90, 145)
    redLow = (0, 10)
    redHigh = (330, 359)
    orange = (15, 40)
    whiteV = (0, 30)
    hsv = cv2.cvtColor(b)
    #tbd

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

testFindDominantColor()
class Face:
    def __init__(face_colors):
        self.colors = face_colors[:][:]
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
    def turn_right():
        top_orientations = [2,1,0,2,2,2,0,1,2,0,0,0]
        bottom_orientations = [0,1,2,2,2,2,2,1,0,0,0,0]
        bottom_color = self.color[1][1]
        if(bottom_color%2 == 0):
            bottom_color = bottom_color + (2*pow((-1),(bottom_color/2+1)))
        row_start = 3 * (bottom_color - 1)
        col_start = (3*bottom_color) % 12
        temp[0] = self.bottom.colors[bottom_orientations[row_start]:bottom_orientations[row_start]+1][bottom_orientations[col_start]:bottom_orientations[col_start]+1]
        temp[1] = self.bottom.colors[bottom_orientations[row_start+1]:bottom_orientations[row_start+1]+1][bottom_orientations[col_start+1]:bottom_orientations[col_start+1]+1]
        temp[2] = self.bottom.colors[bottom_orientations[row_start+2]:bottom_orientations[row_start+2]+1][bottom_orientations[col_start+2]:bottom_orientations[col_start+2]+1]
        row_start = 3 * (self.color[1][1] - 1)
        col_start = (3*self.color[1][1]) % 12
        self.bottom.colors[bottom_orientations[row_start]:bottom_orientations[row_start]+1][bottom_orientations[col_start]:bottom_orientations[col_start]+1] = self.right.right.colors[2][0:1]
        self.bottom.colors[bottom_orientations[row_start+1]:bottom_orientations[row_start+1]+1][bottom_orientations[col_start+1]:bottom_orientations[col_start+1]+1] = self.right.right.colors[1][0:1]
        self.bottom.colors[bottom_orientations[row_start+2]:bottom_orientations[row_start+2]+1][bottom_orientations[col_start+2]:bottom_orientations[col_start+2]+1] = self.right.right.colors[0][0:1]
        self.right.right.colors[0][0] = self.top.colors[top_orientations[row_start]:top_orientations[row_start]+1]][top_orientations[col_start]:top_orientations[col_start]+1]
        self.right.right.colors[1][0] = self.top.colors[top_orientations[row_start+1]:top_orientations[row_start+1]+1]][top_orientations[col_start+1]:top_orientations[col_start+1]+1]
        self.right.right.colors[2][0] = self.top.colors[top_orientations[col_start+2]:top_orientations[col_start+2]+1]][top_orientations[col_start+2]:top_orientations[col_start+2]+1]
        self.top.colors[top_orientations[row_start]:top_orientations[row_start]+1]][top_orientations[col_start]:top_orientations[col_start]+1] =self.colors[0][2:]
        self.top.colors[top_orientations[row_start+1]:top_orientations[row_start+1]+1]][top_orientations[col_start+1]:top_orientations[col_start+1]+1] =self.colors[1][2:]
        self.top.colors[top_orientations[col_start+2]:top_orientations[col_start+2]+1]][top_orientations[col_start+2]:top_orientations[col_start+2]+1] =self.colors[2][2:]
        self.colors[0][2]=temp[0:1]
        self.colors[1][2]=temp[1:2]
        self.colors[2][2]=temp[2:]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = colors[2][0:1]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.right.colors[3-j][i:i+1]
                    temp_index += 1
                self.right.colors[3-j][i]=self.right.colors[i+add_array[i]][3-j:4-j] 
        self.right.colors[0][1] = temp[0:1]
        self.right.colors[0][2] = temp[1:2]
        self.right.colors[1][2] = temp[2:]
        self.right.colors[0][0] = stemp  
    def turn_left():
        top_orientations = [0,1,2,0,0,0,2,1,0,2,2,2]
        bottom_orientations = [2,1,0,2,2,2,0,1,2,0,0,0]
        row_start = 3 * (self.color[1][1] - 1)
        col_start = (9 + 3 * (self.color[1][1] - 1)) % 12
        temp[0] = self.bottom.colors[bottom_orientations[row_start]][bottom_orientations[col_start]:bottom_orientations[col_start] + 1]
        temp[1] = self.bottom.colors[bottom_orientations[row_start + 1]][bottom_orientations[col_start + 1]:bottom_orientations[col_start + 1]+1]
        temp[2] = self.bottom.colors[bottom_orientations[row_start + 2]][bottom_orientations[col_start + 2]:bottom_orientations[col_start + 2] + 1]
        self.bottom.colors[bottom_orientations[row_start]][bottom_orientations[col_start]:bottom_orientations[col_start] + 1] = self.colors[0][0:1]
        self.bottom.colors[bottom_orientations[row_start + 1]][bottom_orientations[col_start + 1]:bottom_orientations[col_start + 1]+1] = self.colors[1][0:1]
        self.bottom.colors[bottom_orientations[row_start + 2]][bottom_orientations[col_start + 2]:bottom_orientations[col_start + 2] + 1] = self.colors[2][0:1]
        row_start = 3 * (self.color[1][1] - 1)
        col_start = (3 * self.color[1][1]) % 12
        self.colors[0][0:1] = self.top.colors[top_orientations[row_start]:top_orientations[row_start]+1]][top_orientations[col_start]:top_orientations[col_start]+1]
        self.colors[1][0:1] = self.top.colors[top_orientations[row_start+1]:top_orientations[row_start+1]+1]][top_orientations[col_start+1]:top_orientations[col_start+1]+1]
        self.colors[2][0:1] = self.top.colors[top_orientations[col_start+2]:top_orientations[col_start+2]+1]][top_orientations[col_start+2]:top_orientations[col_start+2]+1]
        self.top.colors[top_orientations[row_start]:top_orientations[row_start]+1]][top_orientations[col_start]:top_orientations[col_start]+1] = self.left.left.colors[0][2:]
        self.top.colors[top_orientations[row_start+1]:top_orientations[row_start+1]+1]][top_orientations[col_start+1]:top_orientations[col_start+1]+1] = self.left.left.colors[1][2:]
        self.top.colors[top_orientations[col_start+2]:top_orientations[col_start+2]+1]][top_orientations[col_start+2]:top_orientations[col_start+2]+1] = self.left.left.colors[2][2:]
        self.left.left.colors[0][2:] = temp[0:1]
        self.left.left.colors[1][2:] = temp[1:2]
        self.left.left.colors[2][2:] = temp[2:]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = colors[2][0:1]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.left.colors[3-j][i:i+1]
                    temp_index += 1
                self.right.colors[3-j][i]=self.left.colors[i+add_array[i]][3-j:4-j] 
        self.left.colors[0][1] = temp[0:1]
        self.left.colors[0][2] = temp[1:2]
        self.left.colors[1][2] = temp[2:]
        self.left.colors[0][0] = stemp
    def turn_upper():
        temp[0] = self.colors[0][0:1]
        temp[1] = self.colors[0][1:2]
        temp[2] = self.colors[0][2:]
        self.colors[0][0:1] = self.right.colors[0][0:1]
        self.colors[0][1:2] = self.right.colors[0][1:2]
        self.colors[0][2:]  = self.right.colors[0][2:] 
        self.right.colors[0][0:1] = self.right.right.colors[0][0:1]
        self.right.colors[0][1:2] = self.right.right.colors[0][1:2]
        self.right.colors[0][2:] = self.right.right.colors[0][2:] 
        self.right.right.colors[0][0:1] = self.left.colors[0][0:1]
        self.right.right.colors[0][1:2] = self.left.colors[0][1:2]
        self.right.right.colors[0][2:]  = self.left.colors[0][2:] 
        self.left.colors[0][0:1]=temp[0:1]
        self.left.colors[0][1:2]=temp[1:2]
        self.left.colors[0][2:] =temp[2:]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = colors[2][0:1]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.top.colors[3-j][i:i+1]
                    temp_index += 1
                self.top.colors[3-j][i]=self.top.colors[i+add_array[i]][3-j:4-j] 
        self.top.colors[0][1] = temp[0:1]
        self.top.colors[0][2] = temp[1:2]
        self.top.colors[1][2] = temp[2:]
        self.top.colors[0][0] = stemp
    def turn_lower(): 
        temp[0] = self.colors[2][0:1]
        temp[1] = self.colors[2][1:2]
        temp[2] = self.colors[2][2:]
        self.colors[2][0:1] = self.left.colors[2][0:1]
        self.colors[2][1:2] = self.left.colors[2][1:2]
        self.colors[2][2:]  = self.left.colors[2][2:] 
        self.left.colors[2][0:1] = self.right.right.colors[2][0:1]
        self.left.colors[2][1:2] = self.right.right.colors[2][1:2]
        self.left.colors[2][2:]  = self.right.right.colors[2][2:] 
        self.right.right.colors[2][0:1] = self.right.colors[2][0:1]
        self.right.right.colors[2][1:2] = self.right.colors[2][1:2]
        self.right.right.colors[2][2:]  = self.right.colors[2][2:] 
        self.right.colors[0][0:1]=temp[0:1]
        self.right.colors[0][1:2]=temp[1:2]
        self.right.colors[0][2:] =temp[2:]
        temp_index = 0
        add_array = [2,0,-2]
        stemp = colors[2][0:1]
        for i in range(0,3):
            for j in range(1,4):
                if(j!=1 and i != 2):
                    temp_index = temp_index if temp_index != 3 else 2
                    temp[temp_index]=self.bottom.colors[3-j][i:i+1]
                    temp_index += 1
                self.bottom.colors[3-j][i]=self.bottom.colors[i+add_array[i]][3-j:4-j] 
        self.bottom.colors[0][1] = temp[0:1]
        self.bottom.colors[0][2] = temp[1:2]
        self.bottom.colors[1][2] = temp[2:]
        self.bottom.colors[0][0] = stemp