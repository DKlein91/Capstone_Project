from tkinter import ttk
from tkinter import messagebox
from tkinter import *
try:
    from Tkinter import Entry, Frame, Label, StringVar
    from Tkconstants import *
except ImportError:
    from tkinter import Entry, Frame, Label, StringVar
    from tkinter.constants import *

root = Tk()
root.title("WINDOWS FORENSICS SUITE")
root.geometry('500x400')
theLabel = Label(root, text="PREFETCH INSPECTOR",font=("Arial Bold", 30))
theLabel.grid(row=0, column=2)
topFrame = Frame(root)
topFrame.grid(row=0, column=0)
bottomFrame = Frame(root)
bottomFrame.grid(row=15, column=7)

# PROGRESS BAR
#
# pb = ttk.Progressbar(root, orient="horizontal", length=900, mode="determinate")
# pb.grid(row=2,column=2)
# pb.start()

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

# ERROR BOX

#
# def clicked():
#     messagebox.showinfo('Message title', 'Message content')
#
#
# btn = Button(root, text='Click here', command=clicked)
#
# btn.grid(column=1, row=4)
#
# messagebox.showwarning('Message title', 'Warning')  # shows warning message
#
# messagebox.showerror('Message title', 'error')  #shows error mess
#
# res = messagebox.askquestion('Message title', 'Message content')
#
# res = messagebox.askyesno('Message title', 'Yes','No')
#
# res = messagebox.askyesnocancel('Message title', 'Cancel')
#
# res = messagebox.askokcancel('Message title', 'Try ')
#
# res = messagebox.askretrycancel('Message title', 'Message content')




# SEARCHBAR (THE SEARCH BAR AND PRETCH PAGE POPS UP SEPERATE FOR SOMEREASON IDK WHY ?!?)
def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color." % str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))


class Placeholder_State(object):
    __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'


def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")

    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color = normal_color
    state.normal_font = normal_font
    state.placeholder_color = color
    state.placeholder_font = font
    state.placeholder_text = placeholder
    state.contains_placeholder = True

    def on_focusin(event, entry=entry, state=state):
        if state.contains_placeholder:
            entry.delete(0, "end")
            entry.config(fg=state.normal_color, font=state.normal_font)

            state.contains_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg=state.placeholder_color, font=state.placeholder_font)

            state.contains_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg=color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")

    entry.placeholder_state = state

    return state


class SearchBox(Frame):
    def __init__(self, master, entry_width=30, entry_font=None, entry_background="white", entry_highlightthickness=1,
                 button_text="Search", button_ipadx=10, button_background="#009688", button_foreground="white",
                 button_font=None, opacity=0.8, placeholder=None, placeholder_font=None, placeholder_color="grey",
                 spacing=3, command=None):
        Frame.__init__(self, master)

        self._command = command

        self.entry = Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background,
                           highlightthickness=entry_highlightthickness)
        self.entry.grid(row=3,column=3)

        if entry_font:
            self.entry.configure(font=entry_font)

        if placeholder:
            add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

        self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
        self.entry.bind("<Return>", self._on_execute_command)

        opacity = float(opacity)

        if button_background.startswith("#"):
            r, g, b = hex2rgb(button_background)
        else:
            # Color name
            r, g, b = master.winfo_rgb(button_background)

        r = int(opacity * r)
        g = int(opacity * g)
        b = int(opacity * b)

        if r <= 255 and g <= 255 and b <= 255:
            self._button_activebackground = '#%02x%02x%02x' % (r, g, b)
        else:
            self._button_activebackground = '#%04x%04x%04x' % (r, g, b)

        self._button_background = button_background

        self.button_label = Label(self, text=button_text, background=button_background, foreground=button_foreground,
                                  font=button_font)
        if entry_font:
            self.button_label.configure(font=button_font)

        self.button_label.grid(row=3, column=5)

        self.button_label.bind("<Enter>", self._state_active)
        self.button_label.bind("<Leave>", self._state_normal)

        self.button_label.bind("<ButtonRelease-1>", self._on_execute_command)

    def get_text(self):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            if entry.placeholder_state.contains_placeholder:
                return ""
            else:
                return entry.get()
        else:
            return entry.get()

    def set_text(self, text):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            entry.placeholder_state.contains_placeholder = False

        entry.delete(0, END)
        entry.insert(0, text)

    def clear(self):
        self.entry_var.set("")

    def focus(self):
        self.entry.focus()

    def _on_execute_command(self, event):
        text = self.get_text()
        self._command(text)

    def _state_normal(self, event):
        self.button_label.configure(background=self._button_background)

    def _state_active(self, event):
        self.button_label.configure(background=self._button_activebackground)


if __name__ == "__main__":
    try:
        from Tkinter import Tk
        from tkMessageBox import showinfo
    except ImportError:
        from tkinter import Tk
        from tkinter.messagebox import showinfo


    def command(text):
        showinfo("search command", "searching:%s" % text)


    root = Tk()
    SearchBox(root, command=command, placeholder="Type and press enter", entry_highlightthickness=0).grid(row=3,
                                                                                                          column=4)



root.mainloop()