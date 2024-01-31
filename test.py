import tkinter as tk

def button_press(m):
    print("something: " + m)

window = tk.Tk()
window.title("Shapes")
window.geometry("500x400")
mylabel = tk.Label(text = "I love watching Virat Kohli play cricket ")
# mylabel.grid(column=0,row=0)
buttons = [[0 for x in range(4)] for y in range(4)]
for i in range(4):
    for j in range(4):
        test = str(i) + " " + str(j)
        print("this is test" + test)
        buttons[i][j] = tk.Button(window, text = ("Button " + str((i+1)*(j+1))), command=lambda m=test: button_press(m))
        buttons[i][j].grid(column=j,row=i)
window.mainloop()

