import tkinter as tk

root = tk.Tk()

T1 = tk.Text(root)
T1.tag_configure("left", justify='left')
T1.insert("1.0", "A LNK file is a shortcut or link used by Windows as a reference to an orpinal file.")
T1.tag_add("left", "1.0", "end")
T1.pack()

root.mainloop()