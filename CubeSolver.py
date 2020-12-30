#Parameters are each face of the cube as a 3x3 array
#Function returns a string in Cube Notation
def solver(yellow, white, blue, green, red, orange):
class Face:
    def __init__(face_colors):
        self.colors = face_colors[:][:]
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
    def turn_right():
        top_orientations = [0,0,0,2,2,2,0,1,2,2,1,0]
        row = self.color[1][1] * 3 
        temp[0] = self.bottom.colors[0][2:]
        temp[1] = self.bottom.colors[1][2:]
        temp[2] = self.bottom.colors[2][2:]
        self.bottom.colors[0][2:] = self.right.right.colors[2][0:1]
        self.bottom.colors[1][2:] = self.right.right.colors[1][0:1]
        self.bottom.colors[2][2:] = self.right.right.colors[0][0:1]
        self.right.right.colors[0][0] = self.top.colors[2][2:]
        self.right.right.colors[1][0] = self.top.colors[1][2:]
        self.right.right.colors[2][0] = self.top.colors[0][2:]
        self.top.colors[0][2]=self.colors[0][2:]
        self.top.colors[1][2]=self.colors[1][2:]
        self.top.colors[2][2]=self.colors[2][2:]
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
        temp[0] = self.bottom.colors[0][0:1]
        temp[1] = self.bottom.colors[1][0:1]
        temp[2] = self.bottom.colors[2][0:1]
        self.bottom.colors[0][0:1] = self.left.left.colors[2][2:]
        self.bottom.colors[1][0:1] = self.left.left.colors[1][2:]
        self.bottom.colors[2][0:1] = self.left.left.colors[0][2:]
        self.left.left.colors[0][2] = self.top.colors[2][0:1]
        self.left.left.colors[1][2] = self.top.colors[1][0:1]
        self.left.left.colors[2][2] = self.top.colors[0][0:1]
        self.top.colors[0][0]=self.colors[0][0:1]
        self.top.colors[1][0]=self.colors[1][0:1]
        self.top.colors[2][0]=self.colors[2][0:1]
        self.colors[0][0]=temp[0:1]
        self.colors[1][0]=temp[1:2]
        self.colors[2][0]=temp[2:]
        stemp = self.left.colors[0][0:1]
        temp[0] = self.left.colors[1][0:1]
        temp[1] = self.left.colors[2][0:1]
        temp[2] = self.left.colors[2][1:2]
        for i in range(0,3):
            for j in range(0,3):
                self.left.colors[j][i] = self.left.colors[i][2-j:3-j]
        self.left.colors[2][o] = stemp
        self.left.colors[2][1] = temp[0:1]
        self.left.colors[2][2] = temp[1:2]
        self.left.colors[1][2] = temp[2:]
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