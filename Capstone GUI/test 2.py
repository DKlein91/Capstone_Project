import tkinter as tk
from tkinter import font  as tkfont

try:
    from Tkinter import Entry, Frame, Label, StringVar
    from Tkconstants import *
except ImportError:
    from tkinter import Entry, Frame, Label, StringVar
    from tkinter.constants import *
    from tkinter import *
    from tkinter import font  as tkfont
    # Create Window object

    root = Tk()
    root.title("WINDOWS FORENSICS SUITE")
    root.geometry('700x400')
    theLabel = Label(root, text="LNK FILE INSPECTOR", font=("Arial Bold", 30))
    theLabel.grid(row=0, column=2)
    topFrame = Frame(root)
    topFrame.grid(row=0, column=0)
    bottomFrame = Frame(root)
    bottomFrame.grid(row=15, column=7)
    root.configure(background="yellow")


# Page Transitions
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, Select, Settings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Windows Foresics Suite", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Select Inspectors",
                            command=lambda: controller.show_frame("Select"))
        button2 = tk.Button(self, text="Settings",
                            command=lambda: controller.show_frame("Settings"))
        button1.pack()
        button2.pack()


class Select(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Inspectors", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home Page",
                           command=lambda: controller.show_frame("HomePage"))
        button.pack()


class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home Page",
                           command=lambda: controller.show_frame("HomePage"))
        button.pack()



# Search Bar





if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()