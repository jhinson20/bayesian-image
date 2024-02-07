import tkinter as tk

def button_press(m):
    print("something: " + m)

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

buttons = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        test = str(i) + " " + str(j)
        buttons[i][j] = tk.Button(buttonFrame, text = ("Button " + str((i+1)*(j+1))), command=lambda m=test: button_press(m))
        buttons[i][j].grid(column=j,row=i, pady=10, padx=10)

window.mainloop()

