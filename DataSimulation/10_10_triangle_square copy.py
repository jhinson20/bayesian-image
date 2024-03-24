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
