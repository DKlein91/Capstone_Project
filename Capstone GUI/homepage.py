#Import everything from tkinter
from tkinter import *
from tkinter import Menu
import time
import calendar
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import Image


#Create Window object
root = Tk()
root.title("Welcome to WFS")
root.geometry('900x400')
theLabel = Label(root, text="WINDOWS FORENSICS SUITE",font=("Arial Bold", 30))
theLabel.grid(row=0, column=1)
topFrame = Frame(root)
topFrame.grid(row=0, column=0)
bottomFrame = Frame(root)
bottomFrame.grid(row=15, column=7)

# Insert a menu bar on the main window

menu = Menu(root)

new_item = Menu(menu)

new_item.add_command(label='New')

new_item.add_separator()

new_item.add_command(label='Edit')

menu.add_cascade(label='File', menu=new_item)

root.config(menu=menu)

# BACKGROUND OPTIONS (SETTINGS)
root.configure(background='white')
# root.configure(background='grey')
# root.configure(background='blue')

# imageFile = "wfs.png"
#
# root.im1 = Image.open(imageFile)



# FONT SIZE & COLOR
# class SampleApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#     self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
#
#     # the container is where we'll stack a bunch of frames
#     # on top of each other, then the one we want visible
#     # will be raised above the others
#     container = tk.Frame(self)
#     container.pack(side="top", fill="both", expand=True)
#     container.grid_rowconfigure(0, weight=1)
#     container.grid_columnconfigure(0, weight=1)
#
#     self.frames = {}
#     for F in (HomePage, Select, Settings):
#         page_name = F.__name__
#         frame = F(parent=container, controller=self)
#         self.frames[page_name] = frame
#
#         # put all of the pages in the same location;
#         # the one on the top of the stacking order
#         # will be the one that is visible.
#         frame.grid(row=0, column=0, sticky="nsew")
#
#     self.show_frame("HomePage")
#
#
# def show_frame(self, page_name):
#     '''Show a frame for the given page name'''
#     frame = self.frames[page_name]
#     frame.tkraise()


# Page Transitions

# # LOGO
# photo = PhotoImage(file= "/Downloads/page/wfslogo.png")
# label = Label(root, image=photo)
# label.pack()

 # LABELS / Textboxs

entry_1 = Entry(root)
entry_2 = Entry(root)
entry_3 = Entry(root)
entry_4 = Entry(root)
entry_5 = Entry(root)

# textboxs
entry_1.grid(row=4, column=1)
entry_2.grid(row=6, column=1)
# entry_3.grid(row=7, column=2)
entry_4.grid(row=4, column=0)
entry_5.grid(row=6, column=0)


# Text
t1= Label(root, text="FileName:")
t1.grid(row=3, column=1)
t2= Label(root, text="UserName:")
t2.grid(row=5, column=1)
t3= Label(root, text="Start Date:")
t3.grid(row=3, column=0)
t4= Label(root, text="End Date:")
t4.grid(row=5, column=0)
t5= Label(root, text="Sort Results by:",font=("Arial Bold",15))
t5.grid(row=2, column=2)
t6= Label(root, text="Search by date range:",font=("Arial Bold",15))
t6.grid(row=2, column=0)
t7= Label(root, text="Search for specific file & user:",font=("Arial Bold",15))
t7.grid(row=2, column=1)

# CHECKBOX
c1 = Checkbutton(root, text= "Created")
c2 = Checkbutton(root, text= "Modified")
c3 = Checkbutton(root, text= "Deleted")
c4 = Checkbutton(root, text= "Accessed")
c5 = Checkbutton(root, text= "All")

c1.grid(row=3, column=2)
c2.grid(row=4, column=2)
c3.grid(row=5, column=2)
c4.grid(row=6, column=2)
c5.grid(row=7, column=2)

# WIDGETS (BUTTONS) / # Define buttons (Home Page)
button1 = Button(topFrame, text="Select Inspector")
button2 = Button(topFrame, text="Search")
button3 = Button(topFrame, text="Settings")

button1.grid(row=0, column=0)
button2.grid(row=1, column=0)
button3.grid(row=2, column=0)

# SELECT SYSTEM IMAGE
cx1 = Checkbutton(root, text= "Live System")
cx2 = Checkbutton(root, text= "System Image")
# button12 = Button(topFrame, text="Select System Image")

cx1.grid(row=7, column=2)
cx2.grid(row=8, column=3)
# button12.grid(row=6,column=3)

# SORT RESULTS BY
cx3 = Checkbutton(root, text= "Date")
cx4 = Checkbutton(root, text= "Filename")
cx5 = Checkbutton(root, text= "Username")

cx3.grid(row=3, column=3)
cx4.grid(row=4, column=3)
cx5.grid(row=5, column=3)


# CALENDER DATE PICKER (ALOT OF CODE)
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
        self.geometry("+730+390")

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
        DescriptionNotes:
            Get the date from the calendar on button click.

        :param clicked: button clicked event.
        :type clicked: tkinter event
        """

        clicked_button = clicked.widget
        year = self.year_str_var.get()
        month = self.month_str_var.get()
        date = clicked_button['Calender']

        self.full_date = self.str_format % (date, month, year)
        print(self.full_date)

        try:
            self.widget.delete(0, tk.END)
            self.widget.insert(0, self.full_date)
        except AttributeError:
            pass



if __name__ == '__main__':
    def application():
        MyDatePicker(format_str='%02d-%s-%s')
    # calender adjustments
    root = tk.Tk()
    root.title("Start Date")
    root.geometry('200x100')
    btn = tk.Button(root, text="Calender", command=application)
    btn.grid(row=4, column=0)



root.mainloop()



