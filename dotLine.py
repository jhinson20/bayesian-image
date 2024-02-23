import tkinter as tk
import random
import pandas as pd
import os
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

##FF4500 orange
##00BAFF blue
#Dot = 0
#Line = 1

def togglePixel(m):
    row = int(m[:m.index(',')])
    col = int(m[m.index(',') + 1:])
    if matrix[row][col] == 1:
        matrix[row][col] = 0
        buttons[row][col].config(bg="grey")
    else:
        matrix[row][col] = 1
        buttons[row][col].config(bg=_orange)

def shapePress():
    shape = determineShape()

    shapeCanvas.delete("all")
    if shape == 0:
        createDot()
    else:
        createLine()

def clearGrid():
    shapeCanvas.delete("all")
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
                matrix[i][j] = 0
                buttons[i][j].config(bg="grey")

def createDot():
    shapeCanvas.create_rectangle(125, 125, 175, 175, fill=_blue)

def createLine():
    shapeCanvas.create_rectangle(0, 125, 300, 175, fill=_blue)

def saveShape(s):
    nodes = []

    for row in matrix:
        for val in row:
            nodes.append(val)

    dot = {
        'shape': [s]
    }

    dataFrame = pd.DataFrame(dot)

    nodeNames = list("x" + str(i) for i in range(len(nodes)))

    for i in range(len(nodes)):
        dataFrame[nodeNames[i]] = [nodes[i]]

    fileName = 'data/dotLine.csv'

    if os.path.isfile(fileName):
        dataFrame.to_csv(fileName, index=False, header=False, mode='a')
    else:
        dataFrame.to_csv(fileName, index=False, header=True, mode='a')

def determineShape():
    fileName = 'data/dotLine.csv'

    data = pd.read_csv(fileName)

    edges = [('shape', 'x0'), ('shape', 'x1'), ('shape', 'x2'), ('shape', 'x3')]

    graph = BayesianNetwork(edges)
    graph.fit(data)

    infer = VariableElimination(graph)

    nodes = []

    for row in matrix:
        for val in row:
            nodes.append(val)

    evidenceDict = {}

    nodeNames = list("x" + str(i) for i in range(len(nodes)))

    for i in range(len(nodes)):
        evidenceDict[nodeNames[i]] = nodes[i]

    #Gives the probability that the shape is what is says it is
    probability = infer.max_marginal(variables = ["shape"], evidence= evidenceDict)
    shape = str(infer.map_query(variables = ["shape"], evidence= evidenceDict))

    shape = int(shape[shape.find(':') + 1 : shape.rfind('}')].strip())

    return shape
    

_orange = "#FF4500"
_blue = "#00BAFF"

numberRows = 2
numberCols = 2

window = tk.Tk()
window.title("Dots and Lines")
window.geometry("500x400")
window.minsize(height=600, width= 750)
leftFrame = tk.Frame(window, bg=_orange)
leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
rightFrame = tk.Frame(window)
rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
rightFrame.grid_rowconfigure(0, weight=1)
rightFrame.grid_rowconfigure(0, weight=1)
buttonFrame = tk.Frame(rightFrame, width=300, height=200)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)
buttonFrame.columnconfigure(3, weight=1)
buttonFrame.place(in_=rightFrame, anchor="c", relx=.5, rely=.5)
shapeFrame = tk.Frame(leftFrame, bg=_orange, width=300, height=300)
shapeFrame.place(in_=leftFrame, anchor="c", relx=.5, rely=.5)
buttons = [[0 for x in range(numberRows)] for y in range(numberCols)]
matrix = [[0 for x in range(numberRows)] for y in range(numberCols)]

optionsFrame = tk.Frame(rightFrame, height=70)
optionsFrame.pack(side="bottom", fill='x', pady=20)

shapeCanvas = tk.Canvas(shapeFrame, width=300, height=300, bg=_orange, highlightthickness=0)
shapeCanvas.pack()

shapeButton = tk.Button(optionsFrame, text="Shape", command=shapePress)
clearButton = tk.Button(optionsFrame, text="Clear", command=clearGrid)
dotButton = tk.Button(optionsFrame, text="Save Dot", command=lambda m=0: saveShape(m))
lineButton = tk.Button(optionsFrame, text="Save Line", command=lambda m=1: saveShape(m))
optionsFrame.grid_columnconfigure(0, weight=1)
optionsFrame.grid_columnconfigure(1, weight=1)
optionsFrame.grid_columnconfigure(2, weight=1)
optionsFrame.grid_columnconfigure(3, weight=1)
shapeButton.grid(row=0, column=0)
clearButton.grid(row=0, column=1)
dotButton.grid(row=0, column=2)
lineButton.grid(row=0, column=3)

for i in range(len(buttons)):
    for j in range(len(buttons[0])):
        rowCol = str(i) + ',' + str(j)
        buttons[i][j] = tk.Button(buttonFrame, command=lambda m=rowCol: togglePixel(m), height=2, width=5, bg="grey")
        buttons[i][j].grid(column=j,row=i, pady=10, padx=10)

window.mainloop()