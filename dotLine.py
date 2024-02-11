import tkinter as tk
import random
import pandas as pd

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
    randInt = random.randint(0, 1)

    shapeCanvas.delete("all")
    if randInt == 0:
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

def saveDot():
    nodes = []

    for row in matrix:
        for val in row:
            nodes.append(val)

    dot = {
        'shape': 0,
    }

    i = 0
    for node in nodes:
        series = pd.Series(node, index = ["x" + str(i)])
        pd.concat([dot, series.to_frame()], axis=1)
        i += 1    
    
    print(dot)
    print("save dot")

def saveLine():
    print("save line")

_orange = "#FF4500"
_blue = "#00BAFF"

numberRows = 2
numberCols = 2

window = tk.Tk()
window.title("Dots and Lines")
window.geometry("500x400")
window.minsize(height=600, width= 700)
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
dotButton = tk.Button(optionsFrame, text="Save Dot", command=saveDot)
lineButton = tk.Button(optionsFrame, text="Save Line", command=saveLine)
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