import tkinter as tk
import pandas as pd
import os
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete.CPD import TabularCPD

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
    shape, probability = determineShape()
    updateProbabilites(shape, probability)

    shapeCanvas.delete("all")
    if shape == 0:
        createDot()
    else:
        createLine()

def updateProbabilites(shape, probability):
    higherPercentage = str(round(probability*100, 2)) + "%"
    lowerPercentage = str(round((1 - probability)*100, 2)) + "%"

    if shape == 0:
        dotProbability.config(text=higherPercentage)
        lineProbability.config(text=lowerPercentage)
    else:
        dotProbability.config(text=lowerPercentage)
        lineProbability.config(text=higherPercentage)



def clearGrid():
    shapeCanvas.delete("all")
    dotProbability.config(text="0%")
    lineProbability.config(text="0%")
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
    print(shape)

    shape = int(shape[shape.find(':') + 1 : shape.rfind('}')].strip())

    return shape, probability
    

_orange = "#FF4500"
_blue = "#00BAFF"

numberRows = 2
numberCols = 2

matrix = [[0 for x in range(numberRows)] for y in range(numberCols)]

#Creates the window and sets min size
window = tk.Tk()
window.title("Dots and Lines")
window.geometry("500x400")
window.minsize(height=600, width= 1200)

#Creates left and right frames the window will be split by
rightFrame = tk.Frame(window, bg=_orange, width=400)
rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
leftFrame = tk.Frame(window)
leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
leftFrame.grid_rowconfigure(0, weight=1)

#Creates elements within the left frame
buttonFrame = tk.Frame(leftFrame, height=200)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)
buttonFrame.columnconfigure(3, weight=1)
buttonFrame.place(in_=leftFrame, anchor="c", relx=.5, rely=.5)
buttons = [[0 for x in range(numberRows)] for y in range(numberCols)]

optionsFrame = tk.Frame(leftFrame, height=70)
optionsFrame.pack(side="bottom", fill='x', pady=20)

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

#Creates elements in the right frame
shapeFrame = tk.Frame(rightFrame, bg=_orange, width=100)
shapeFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
shapeOutline = tk.Frame(shapeFrame, bg=_orange, height=300, width=90)
shapeOutline.place(in_=shapeFrame, anchor="c", relx=.5, rely=.5, relwidth=0.95)
shapeCanvas = tk.Canvas(shapeOutline, width=300, height=300, bg=_orange, highlightthickness=0)
shapeCanvas.pack()

probabilityFrame = tk.Frame(rightFrame, bg=_blue, width=100)
probabilityFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
topFrame = tk.Frame(probabilityFrame, bg=_blue, height=100, width=100)
topFrame.grid(row=0, column=0, sticky="nsew")
bottomFrame = tk.Frame(probabilityFrame, bg=_blue, height=100, width=100)
bottomFrame.grid(row=1, column=0, sticky="nsew")
probabilityFrame.columnconfigure(0, weight=1)  
probabilityFrame.rowconfigure(0, weight=1)     
probabilityFrame.rowconfigure(1, weight=1)

dotProbability = tk.Label(topFrame, text="0%", bg=_blue)
dotProbability.place(relx=0.5, rely=.1)
dotCanvasOultine = tk.Frame(topFrame, bg=_blue, height=90, width=90)
dotCanvasOultine.place(in_=topFrame, anchor="c", relx=.5, rely=.5, relwidth=0.95)
dotProbabilityCanvas = tk.Canvas(dotCanvasOultine, width=100, height=100, bg=_blue, highlightthickness=0)
dotProbabilityCanvas.pack()
dotProbabilityCanvas.create_rectangle(30, 30, 70, 70, fill=_orange)

lineProbability = tk.Label(bottomFrame, text="0%", bg=_blue)
lineProbability.place(relx=0.5, rely=.1)
lineCanvasOultine = tk.Frame(bottomFrame, bg=_blue, height=90, width=160)
lineCanvasOultine.place(in_=bottomFrame, anchor="c", relx=.5, rely=.5, relwidth=0.95)
lineProbabilityCanvas = tk.Canvas(lineCanvasOultine, width=160, height=100, bg=_blue, highlightthickness=0)
lineProbabilityCanvas.pack()
lineProbabilityCanvas.create_rectangle(0, 30, 160, 70, fill=_orange)

#Creates file object
fileName = 'data/dotLine.csv'

data = pd.read_csv(fileName)

#Creates the bayesian network
edges = [('shape', 'x0'), ('shape', 'x1'), ('shape', 'x2'), ('shape', 'x3')]

graph = BayesianNetwork(edges)
graph.fit(data, state_names={'shape': [0, 1]})
shape_cpd = TabularCPD('shape', 2, [[0.5],[0.5]])
graph.add_cpds(shape_cpd)

infer = VariableElimination(graph)

#print(infer.query(variables = ["shape"]))

window.mainloop()