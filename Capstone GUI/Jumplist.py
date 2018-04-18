from tkinter import ttk
from tkinter import messagebox
from tkinter import *

root = Tk()
root.title("WINDOWS FORENSICS SUITE")
root.geometry('1120x400')
theLabel = Label(root, text="JUMP LIST INSPECTOR",font=("Arial Bold", 30))
theLabel.grid(row=0, column=2)
topFrame = Frame(root)
topFrame.grid(row=0, column=0)
bottomFrame = Frame(root)
bottomFrame.grid(row=15, column=7)

# PROGRESS BAR

pb = ttk.Progressbar(root, orient="horizontal", length=900, mode="determinate")
pb.grid(row=2,column=2)
pb.start()

# TEXT
t2= Label(root, text="WORDS HERE:")
t2.grid(row=5, column=1)

selected = IntVar()

rad1 = Radiobutton(root, text='Live System', value=1, variable=selected)

rad2 = Radiobutton(root, text='System Image', value=2, variable=selected)

# Buttons
def clicked():
    print(selected.get())


btn1 = Button(root, text="Select System Image", command=clicked)
btn2 = Button(root, text="Run Inspector", command=clicked)

rad1.grid(column=2, row=6)

rad2.grid(column=2, row=7)



btn1.grid(column=2, row=8)
btn2.grid(column=1, row=7)


root.mainloop()