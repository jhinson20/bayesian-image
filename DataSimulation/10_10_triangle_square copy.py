# This file creates a dataset in a csv file in the /data folder that defines many squares and triangles
#All shapes are outlined and not filled

import os
import pandas as pd

_numRowCol = 10

#A 1d array representing the 10x10 grid for entering shapes; created with all 0
grid0 = [0] * _numRowCol**2

fileName = 'data/squareTriangle.csv'

#If the file exists, delete it to generate the data over again
if os.path.isfile(fileName):
    os.remove(fileName)

#Creates an array that will store all of the different sized squares starting at the top left of the input matrix
_startingSquares = []

for i in range(2, _numRowCol + 1):
    square = list(grid0)
    for j in range(i):
        square[j] = 1
        square[j + 10 * i - 10] = 1
        square[j * 10] = 1
        square[j * 10 + i - 1] = 1
        
    _startingSquares.append(square)

#Creates an array that will store all of the different sized triangles starting at the top left of the input matrix
_startingTriangles = []

#Base 3 triangels

triangle = list(grid0)
triangle[1] = 1
triangle[10] = 1
triangle[11] = 1
triangle[12] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[10] = 1
triangle[11] = 1
triangle[20] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[1] = 1
triangle[2] = 1
triangle[11] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[1] = 1
triangle[10] = 1
triangle[11] = 1
triangle[21] = 1
_startingTriangles.append(triangle)

#Base 5 triangels

triangle = list(grid0)
triangle[2] = 1
triangle[11] = 1
triangle[13] = 1
triangle[20] = 1
triangle[21] = 1
triangle[22] = 1
triangle[23] = 1
triangle[24] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[10] = 1
triangle[11] = 1
triangle[20] = 1
triangle[22] = 1
triangle[30] = 1
triangle[31] = 1
triangle[40] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[2] = 1
triangle[11] = 1
triangle[12] = 1
triangle[20] = 1
triangle[22] = 1
triangle[31] = 1
triangle[32] = 1
triangle[42] = 1
_startingTriangles.append(triangle)

#Base 7 triangles

triangle = list(grid0)
triangle[3] = 1
triangle[12] = 1
triangle[14] = 1
triangle[21] = 1
triangle[25] = 1
triangle[30] = 1
triangle[31] = 1
triangle[32] = 1
triangle[33] = 1
triangle[34] = 1
triangle[35] = 1
triangle[36] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[3] = 1
triangle[12] = 1
triangle[13] = 1
triangle[21] = 1
triangle[23] = 1
triangle[30] = 1
triangle[33] = 1
triangle[41] = 1
triangle[43] = 1
triangle[52] = 1
triangle[53] = 1
triangle[63] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[1] = 1
triangle[2] = 1
triangle[3] = 1
triangle[4] = 1
triangle[5] = 1
triangle[6] = 1
triangle[11] = 1
triangle[15] = 1
triangle[22] = 1
triangle[24] = 1
triangle[33] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[10] = 1
triangle[11] = 1
triangle[20] = 1
triangle[22] = 1
triangle[30] = 1
triangle[33] = 1
triangle[40] = 1
triangle[42] = 1
triangle[50] = 1
triangle[51] = 1
triangle[60] = 1
_startingTriangles.append(triangle)

#Base 9 triangles

triangle = list(grid0)
triangle[4] = 1
triangle[13] = 1
triangle[15] = 1
triangle[22] = 1
triangle[26] = 1
triangle[31] = 1
triangle[37] = 1
triangle[40] = 1
triangle[41] = 1
triangle[42] = 1
triangle[43] = 1
triangle[44] = 1
triangle[45] = 1
triangle[46] = 1
triangle[47] = 1
triangle[48] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[4] = 1
triangle[13] = 1
triangle[14] = 1
triangle[22] = 1
triangle[24] = 1
triangle[31] = 1
triangle[34] = 1
triangle[40] = 1
triangle[44] = 1
triangle[51] = 1
triangle[54] = 1
triangle[62] = 1
triangle[64] = 1
triangle[73] = 1
triangle[74] = 1
triangle[84] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[1] = 1
triangle[2] = 1
triangle[3] = 1
triangle[4] = 1
triangle[5] = 1
triangle[6] = 1
triangle[7] = 1
triangle[8] = 1
triangle[11] = 1
triangle[17] = 1
triangle[22] = 1
triangle[26] = 1
triangle[33] = 1
triangle[35] = 1
triangle[44] = 1
_startingTriangles.append(triangle)

triangle = list(grid0)
triangle[0] = 1
triangle[10] = 1
triangle[11] = 1
triangle[20] = 1
triangle[22] = 1
triangle[30] = 1
triangle[33] = 1
triangle[40] = 1
triangle[44] = 1
triangle[50] = 1
triangle[53] = 1
triangle[60] = 1
triangle[62] = 1
triangle[70] = 1
triangle[71] = 1
triangle[80] = 1
_startingTriangles.append(triangle)

#Creates a dataframe with specified columns

_nodeNames = list("x" + str(i) for i in range(_numRowCol**2))
_dataFrame = pd.DataFrame(columns=['shape'] + _nodeNames)

#Functions for moving shapes around the grid

def shiftRight(grid):
    enable = False
    outOfBounds = False
    active = grid.count(1)

    for i in range(len(grid)):
        if grid[i] == 1:
            if not enable:
                grid[i] = 0
            enable = True
        else:
            if enable:
                grid[i] = 1
                if i % _numRowCol == 0:
                    outOfBounds = True
            enable = False

    if active != grid.count(1):
        outOfBounds = True
    
    return grid, outOfBounds

def shiftDown(grid):
    enableList = []
    outOfBounds = False

    for i in range(len(grid)):
        if grid[i] == 1:
            if i not in enableList:
                grid[i] = 0
            enableList.append(i+10)
        else:
            if i in enableList:
                grid[i] = 1
                if i > (_numRowCol**2) - 1:
                    outOfBounds = True
                enableList.remove(i)
    
    return grid, outOfBounds


#Loops that move the shape around the grid

for square in _startingSquares:
    grid = list(square)
    _active = grid.count(1)
    for i in range(_numRowCol):
        beforeRightShift = list(grid)
        for j in range(_numRowCol):

            square = {'shape': 0}

            for j in range(_numRowCol**2):
                square[_nodeNames[j]] = grid[j]

            _dataFrame.loc[len(_dataFrame)] = square
            grid, outOfBounds = shiftRight(grid)
            
            if(outOfBounds):
                break
        grid, outOfBounds = shiftDown(beforeRightShift)

        if outOfBounds or _active != grid.count(1):
            break

if os.path.isfile(fileName):
    _dataFrame.to_csv(fileName, index=False, header=False, mode='a')
else:
    _dataFrame.to_csv(fileName, index=False, header=True, mode='a')
