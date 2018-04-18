from tkinter import *
from PIL import ImageTk, Image
import os
from tkinter import ttk
import calendar
import time
import tkinter as tk
try:
    from Tkinter import Entry, Frame, Label, StringVar
    from Tkconstants import *
except ImportError:
    from tkinter import Entry, Frame, Label, StringVar
    from tkinter.constants import *
    from tkinter import *
    from tkinter import font  as tkfont

# Import Logo
# root = Tk()
# img = ImageTk.PhotoImage(Image.open("True1.gif"))
# panel = Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")

#Create Window object
root = Tk()
root.title("Welcome to WFS")
root.geometry('900x400')
theLabel = Label(root, text="WINDOWS FORENSICS SUITE",font=("Arial Bold", 30))
theLabel.pack()
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack()
note = ttk.Notebook(root)
root.configure(background="white")

# BUTTONS
tab_control = ttk.Notebook(root)

tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
# look for button control


tab_control.add(tab2, text='Home')
tab_control.add(tab3, text='Inspectors')
tab_control.add(tab4, text='Settings')


lbl1 = Label(tab2, text='Start Date: ')
lbl1.grid(column=0, row=0)

# ent = Entry(root)
# ent.grid(column=0,row=1)


lbl2 = Label(tab2, text='End Date: ',font=("Bold"))
lbl2.grid(column=0, row=6)

lbl3 = Label(tab3, text='Select Inspector:', justify='center')
lbl3.grid(column=0, row=0)

lbl4 = Label(tab4, text='Background Color:')
lbl4.grid(column=1, row=2)

lbl5 = Label(tab2, text='FileName:',font=("Bold"))
lbl5.grid(column=3, row=0)

lbl6 = Label(tab2, text='UserName:',font=("Bold"))
lbl6.grid(column=3, row=6)

lbl7 = Label(tab2, text='Sort Results by:', font=("Bold"))
lbl7.grid(column=0, row=12, pady=50)
#
# lbl8= Label(tab3, text='Select System Image:', font=("Bold"))
# lbl8.grid(column=0, row=9)

tab_control.pack(expand=1, fill='both')
# Buttons inside Home
tab1 = Frame(note)
b = Button(tab2, text="Search")
b.grid(row=13,column=2,padx=95)
# b.pack()

Button(tab1, text='Live', command=root.destroy)

#  # LABELS / Textboxs
entry_1 = Entry(tab2)
entry_2 = Entry(tab2)
entry_3 = Entry(tab2)
entry_4 = Entry(tab2)
entry_5 = Entry(tab2)

# # textboxs
entry_1.grid(row=3,column=0)
entry_2.grid(row=7,column=0)
entry_3.grid(row=3, column=3)
entry_4.grid(row=7, column=3)
# entry_5.grid(row=6, column=4)

# Inspectors
button1 = Button(tab3, text="Prefetch File")
button2 = Button(tab3, text=".LNK File")
button3 = Button(tab3, text="Jump List")
# button4 = Button(tab3, text="Index.dat")
# button5 = Button(tab3, text="Logfile")
button6 = Button(tab3, text="Shellbag")
button7 = Button(tab3, text="USN Journal")
button8 = Button(tab3, text="Windows Trash")
button9 = Button(tab3, text="AppCompatCache")

button1.grid(row=9, column=0, pady= (100,100))
button2.grid(row=9, column=1)
button3.grid(row=9, column=2)
# button4.grid(row=6, column=2)
# button5.grid(row=6, column=3)
button6.grid(row=9, column=3)
button7.grid(row=9, column=4)
button8.grid(row=9, column=5)
button9.grid(row=9, column=6)

# SORT RESULTS BY:
cx3 = Checkbutton(tab2, text= "Date")
cx4 = Checkbutton(tab2, text= "Filename")
cx5 = Checkbutton(tab2, text= "Username")

cx3.grid(row=12, column=1,padx=20)
cx4.grid(row=12, column=2, padx=20)
cx5.grid(row=12, column=3)

# CHECKBOX

c1 = Checkbutton(tab2, text= "Created")
c2 = Checkbutton(tab2, text= "Modified")
c3 = Checkbutton(tab2, text= "Deleted")
c4 = Checkbutton(tab2, text= "Accessed")
c5 = Checkbutton(tab2, text= "All")

c1.grid(row=3, column=8,)
c2.grid(row=4, column=8)
c3.grid(row=5, column=8)
c4.grid(row=6, column=8)
c5.grid(row=7, column=8)

# MENU

menu = Menu(root)
new_item = Menu(menu)
new_item.add_command(label='New')
new_item.add_separator()
new_item.add_command(label='Edit')
menu.add_cascade(label='File', menu=new_item)
root.config(menu=menu)

# Settings Radio Buttons

selected = IntVar()

rad1 = Radiobutton(tab4, text='White', value=1, variable=selected)
rad2 = Radiobutton(tab4, text='Grey', value=2, variable=selected)
rad3 = Radiobutton(tab4, text='Blue', value=3, variable=selected)

# Select Image Buttons
rad4 = Radiobutton(tab3, text='Live System', value=1, variable=selected)
rad5 = Radiobutton(tab3, text='System Image', value=2, variable=selected)


def clicked():
    print(selected.get())

btn = Button(tab4, text="Submit", command=clicked)

rad1.grid(row=3,column=3,pady=10,padx=60)
rad2.grid(row=3,column=4,pady=10, padx=60)
rad3.grid(row=3,column=5,pady=10, padx=60)

rad4.grid(row=0, column=3, pady=(10))
rad5.grid(row=0, column=4)

btn.grid(row=10,column=4,pady=30, padx= 30)

# Calendar
class MyDatePicker(tk.Toplevel):
    """
    Description:
        A tkinter GUI date picker.
    """

    def __init__(self, widget=None, format_str=None):
        """
        :param widget: widget of parent instance.

        :param format_str: print format in which to display date.
        :type format_str: string

        Example::
            a = MyDatePicker(self, widget=self.parent widget,
                             format_str='%02d-%s-%s')
        """

        super().__init__()
        self.widget = widget
        self.str_format = format_str

        self.title("Date Picker")
        self.resizable(0, 0)
        self.geometry("+630+390")

        self.init_frames()
        self.init_needed_vars()
        self.init_month_year_labels()
        self.init_buttons()
        self.space_between_widgets()
        self.fill_days()
        self.make_calendar()

    def init_frames(self):
        self.frame1 = tk.Frame(self)
        self.frame1.pack()

        self.frame_days = tk.Frame(self)
        self.frame_days.pack()

    def init_needed_vars(self):
        self.month_names = tuple(calendar.month_name)
        self.day_names = tuple(calendar.day_abbr)
        self.year = time.strftime("%Y")
        self.month = time.strftime("%B")

    def init_month_year_labels(self):
        self.year_str_var = tk.StringVar()
        self.month_str_var = tk.StringVar()

        self.year_str_var.set(self.year)
        self.year_lbl = tk.Label(self.frame1, textvariable=self.year_str_var,
                                 width=3)
        self.year_lbl.grid(row=0, column=5)

        self.month_str_var.set(self.month)
        self.month_lbl = tk.Label(self.frame1, textvariable=self.month_str_var,
                                  width=8)
        self.month_lbl.grid(row=0, column=1)

    def init_buttons(self):
        self.left_yr = ttk.Button(self.frame1, text="←", width=5,
                                  command=self.prev_year)
        self.left_yr.grid(row=0, column=4)

        self.right_yr = ttk.Button(self.frame1, text="→", width=5,
                                   command=self.next_year)
        self.right_yr.grid(row=0, column=6)

        self.left_mon = ttk.Button(self.frame1, text="←", width=5,
                                   command=self.prev_month)
        self.left_mon.grid(row=0, column=0)

        self.right_mon = ttk.Button(self.frame1, text="→", width=5,
                                    command=self.next_month)
        self.right_mon.grid(row=0, column=2)

    def space_between_widgets(self):
        self.frame1.grid_columnconfigure(3, minsize=40)

    def prev_year(self):
        self.prev_yr = int(self.year_str_var.get()) - 1
        self.year_str_var.set(self.prev_yr)

        self.make_calendar()

    def next_year(self):
        self.next_yr = int(self.year_str_var.get()) + 1
        self.year_str_var.set(self.next_yr)

        self.make_calendar()

    def prev_month(self):
        index_current_month = self.month_names.index(self.month_str_var.get())
        index_prev_month = index_current_month - 1

        #  index 0 is empty string, use index 12 instead,
        # which is index of December.
        if index_prev_month == 0:
            self.month_str_var.set(self.month_names[12])
        else:
            self.month_str_var.set(self.month_names[index_current_month - 1])

        self.make_calendar()

    def next_month(self):
        index_current_month = self.month_names.index(self.month_str_var.get())

        try:
            self.month_str_var.set(self.month_names[index_current_month + 1])
        except IndexError:
            #  index 13 does not exist, use index 1 instead, which is January.
            self.month_str_var.set(self.month_names[1])

        self.make_calendar()

    def fill_days(self):
        col = 0
        #  Creates days label
        for day in self.day_names:
            self.lbl_day = tk.Label(self.frame_days, text=day)
            self.lbl_day.grid(row=0, column=col)
            col += 1

    def make_calendar(self):
        #  Delete date buttons if already present.
        #  Each button must have its own instance attribute for this to work.
        try:
            for dates in self.m_cal:
                for date in dates:
                    if date == 0:
                        continue

                    self.delete_buttons(date)

        except AttributeError:
            pass

        year = int(self.year_str_var.get())
        month = self.month_names.index(self.month_str_var.get())
        self.m_cal = calendar.monthcalendar(year, month)

        #  build dates buttons.
        for dates in self.m_cal:
            row = self.m_cal.index(dates) + 1
            for date in dates:
                col = dates.index(date)

                if date == 0:
                    continue

                self.make_button(str(date), str(row), str(col))

    def make_button(self, date, row, column):
        """
        Description:
            Build a date button.

        :param date: date.
        :type date: string

        :param row: row number.
        :type row: string

        :param column: column number.
        :type column: string
        """
        exec(
            "self.btn_" + date + " = ttk.Button(self.frame_days, text=" + date
            + ", width=5)\n"
            "self.btn_" + date + ".grid(row=" + row + " , column=" + column
            + ")\n"
            "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
        )

    def delete_buttons(self, date):
        """
        Description:
            Delete a date button.

        :param date: date.
        :type: string
        """
        exec(
            "self.btn_" + str(date) + ".destroy()"
        )

    def get_date(self, clicked=None):
        """
        Description:
            Get the date from the calendar on button click.

        :param clicked: button clicked event.
        :type clicked: tkinter event
        """

        clicked_button = clicked.widget
        year = self.year_str_var.get()
        month = self.month_str_var.get()
        date = clicked_button['text']

        self.full_date = self.str_format % (date, month, year)
        print(self.full_date)
        #  Replace with parent 'widget' of your choice.
        try:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, self.full_date)
        except AttributeError:
            pass


if __name__ == '__main__':
    def application():
        MyDatePicker(format_str='%02d-%s-%s')
    # Calendar postion on GUI

    btn = tk.Button(tab2, text="Calendar", command=application)
    btn.grid(row=3,column=1)

    btn = tk.Button(tab2, text="Calendar", command=application)
    btn.grid(row=7,column=1)


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


    class Inspectors(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            label = tk.Label(self, text="Windows Foresics Suite", font=controller.title_font)
            label.pack(side="top", fill="x", pady=10)

            button1 = tk.Button(self, text="Select Inspectors",
                                command=lambda: controller.show_frame("Select"))
            button2 = tk.Button(self, text="Settings",
                                command=lambda: controller.show_frame("Settings"))
            button3 = tk.Button(self, text="Settings",
                                command=lambda: controller.show_frame("Settings"))
            button4 = tk.Button(self, text="Settings",
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

#  Insert inspector code 

root.mainloop()