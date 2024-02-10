import tkinter as tk
import random

##FF4500 orange
##00BAFF blue

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
        createTriangle()
    else:
        createSquare()

def clearGrid():
    shapeCanvas.delete("all")
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
                matrix[i][j] = 0
                buttons[i][j].config(bg="grey")

def createTriangle():
    shapeCanvas.create_polygon(150, 0, 0, 300, 300, 300, fill=_blue)

def createSquare():
    shapeCanvas.create_rectangle(0, 0, 300, 300, fill=_blue)

_orange = "#FF4500"
_blue = "#00BAFF"

numberRows = 5
numberCols = 5
window = tk.Tk()
window.title("Squares and Triangles")
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
optionsFrame.grid_columnconfigure(0, weight=1)
optionsFrame.grid_columnconfigure(1, weight=1)
shapeButton.grid(row=0, column=0)
clearButton.grid(row=0, column=1)

for i in range(len(buttons)):
    for j in range(len(buttons[0])):
        rowCol = str(i) + ',' + str(j)
        buttons[i][j] = tk.Button(buttonFrame, command=lambda m=rowCol: togglePixel(m), height=2, width=5, bg="grey")
        buttons[i][j].grid(column=j,row=i, pady=10, padx=10)

window.mainloop()