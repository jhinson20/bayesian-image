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

#Creates a 1d array representing a 2x2 square in the top left corner of the grid
smallSquare = list(grid0)
smallSquare[0] = 1
smallSquare[1] = 1
smallSquare[_numRowCol] = 1
smallSquare[_numRowCol + 1] = 1

#Creates a dataframe with specified columns

_nodeNames = list("x" + str(i) for i in range(_numRowCol**2))
_dataFrame = pd.DataFrame(columns=['shape'] + _nodeNames)

#Represents the lowest rightmost pixel on the shape
_x = [_numRowCol - 1, 1]

#Represents the highest leftmost pixel on the shape
_y = [_numRowCol - 2, 0]

#Functions for moving shapes around the grid

def shiftRight(grid):
    enable = False
    outOfBounds = False

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
    
    return grid, outOfBounds

def shiftDown(grid):
    enableList = []
    # hitBounds = False
    outOfBounds = False

    for i in range(len(grid)):
        if grid[i] == 1:
            if i not in enableList:
                grid[i] = 0
            enableList.append(i+10)
        else:
            if i in enableList:
                grid[i] = 1
                # if _numRowCol*(_numRowCol-1) <= i <= (_numRowCol**2) - 1:
                    # hitBounds = True
                # elif i > (_numRowCol**2) - 1:
                if i > (_numRowCol**2) - 1:
                    outOfBounds = True
                enableList.remove(i)
    
    # return grid, hitBounds, outOfBounds
    return grid, outOfBounds


#Loops that move the shape around the grid

grid = list(smallSquare)
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

# for j in range(_numRowCol):

#     square = {'shape': 0}

#     for j in range(_numRowCol**2):
#         square[_nodeNames[j]] = grid[j]

#     _dataFrame.loc[len(_dataFrame)] = square
#     grid, outOfBounds = shiftRight(grid)
    
#     if(outOfBounds):
#         break

    

if os.path.isfile(fileName):
    _dataFrame.to_csv(fileName, index=False, header=False, mode='a')
else:
    _dataFrame.to_csv(fileName, index=False, header=True, mode='a')
