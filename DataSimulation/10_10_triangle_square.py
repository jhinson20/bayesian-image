# This file creates a dataset in a csv file in the /data folder that defines many squares and triangles

import os
import pandas as pd

_numRowCol = 10

grid0 = [[0 for y in range(_numRowCol)] for x in range(_numRowCol)]

fileName = 'data/squareTriangle.csv'

#If the file exists, delete it to generate the data over again
if os.path.isfile(fileName):
    os.remove(fileName)

#Creates a 2d array representing a 2x2 square in the bottom left corner of the grid
smallSquare = [[0 for y in range(_numRowCol)] for x in range(_numRowCol)]
smallSquare[_numRowCol - 1][0] = 1
smallSquare[_numRowCol - 1][1] = 1
smallSquare[_numRowCol - 2][0] = 1
smallSquare[_numRowCol - 2][1] = 1

#Adds the shape to the file
nodes = []

for row in smallSquare:
    for val in row:
        nodes.append(val)

square = {
    'shape': [0]
}

dataFrame = pd.DataFrame(square)

nodeNames = list("x" + str(i) for i in range(_numRowCol**2))

for i in range(_numRowCol**2):
    dataFrame[nodeNames[i]] = [nodes[i]]

dataFrame.to_csv(fileName, index=False, header=True, mode='a')

#Represents the lowest rightmost pixel on the shape
_x = [_numRowCol - 1, 1]

#Represents the highest leftmost pixel on the shape
_y = [_numRowCol - 2, 0]

#Functions for moving shapes around the grid

def shiftRight(grid):
    enable = False

    for i in range(_numRowCol):
        for j in range(_numRowCol):
            if grid[i][j] == 1:
                if not enable:
                    grid[i][j] = 0
                enable = True
            else:
                if enable:
                    grid[i][j] = 1
                enable = False
    
    return grid


#Loops that move the shape around the grid

grid = list(smallSquare)

for i in range(_numRowCol):
    grid = shiftRight(grid)

    if i == 8:
        print(grid)

#while(_x < _numRowCol and _y < _numRowCol):

# for i in range(_numRowCol):
#     for j in range(_numRowCol):
        
#         if(grid[])