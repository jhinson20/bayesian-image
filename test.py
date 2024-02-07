import tkinter as tk
from tkinter import PhotoImage

def button_press(m):
    row = int(m[:m.index(',')])
    col = int(m[m.index(',') + 1:])
    #buttons[row][col] = 1
    if matrix[row][col] == 1:
        matrix[row][col] = 0
        buttons[row][col].config(bg="grey")
    else:
        matrix[row][col] = 1
        buttons[row][col].config(bg="red")

numberRows = 5
numberCols = 5
window = tk.Tk()
window.title("Shapes")
window.geometry("500x400")
window.minsize(height=600, width= 700)
leftFrame = tk.Frame(window, bg="lightblue")
leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
rightFrame = tk.Frame(window)
rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
rightFrame.grid_rowconfigure(0, weight=1)
rightFrame.grid_rowconfigure(0, weight=1)
buttonFrame = tk.Frame(rightFrame, bg="lightblue", width=300, height=200)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)
buttonFrame.columnconfigure(3, weight=1)
buttonFrame.place(in_=rightFrame, anchor="c", relx=.5, rely=.5)
buttons = [[0 for x in range(numberRows)] for y in range(numberCols)]
matrix = [[0 for x in range(numberRows)] for y in range(numberCols)]


redCircle = PhotoImage(file="images/red_circle.png")
whiteCircle = PhotoImage(file="images/white_circle.png")

for i in range(len(buttons)):
    for j in range(len(buttons[0])):
        rowCol = str(i) + ',' + str(j)
        #buttons[i][j] = tk.Button(buttonFrame, text = ("Button " + str((i+1)*(j+1))), command=lambda m=test: button_press(m), image=whiteCircle, height=50, width=50)
        buttons[i][j] = tk.Button(buttonFrame, command=lambda m=rowCol: button_press(m), height=2, width=5, bg="grey")
        buttons[i][j].grid(column=j,row=i, pady=10, padx=10)

window.mainloop()