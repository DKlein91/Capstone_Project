from tkinter import *

from tkinter import ttk
import calendar
import time
import datetime

import tkinter as tk
try:
    from Tkinter import Entry, Frame, Label, StringVar
    from Tkconstants import *
except ImportError:
    from tkinter import Entry, Frame, Label, StringVar
    from tkinter.constants import *
    from tkinter import *
    from tkinter import font  as tkfont
try:
    import Tkinter
    import tkFont
    import ttk

    from Tkconstants import CENTER, LEFT, N, E, W, S
    from Tkinter import StringVar
except ImportError: # py3k
    import tkinter as Tkinter
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

    from tkinter.constants import CENTER, LEFT, N, E, W, S
    from tkinter import StringVar
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


lbl2 = Label(tab2, text='End Date: ')
lbl2.grid(column=0, row=6)

lbl3 = Label(tab3, text='Select Inspector:', justify='center')
lbl3.grid(column=0, row=0)

lbl4 = Label(tab4, text='Background Color:')
lbl4.grid(column=1, row=2)

lbl5 = Label(tab2, text='FileName:')
lbl5.grid(column=5, row=0)

lbl6 = Label(tab2, text='UserName:')
lbl6.grid(column=5, row=6)

tab_control.pack(expand=1, fill='both')
# Buttons inside Home
tab1 = Frame(note)
b = Button(root, text="Search")
b.pack()

Button(tab1, text='Live', command=root.destroy)

# Text
# t1= Label(tab1, text="FileName:")
# t1.grid(row=3, column=1)
# t2= Label(tab1, text="UserName:")
# t2.grid(row=5, column=1)
# t3= Label(tab2, text="Start Date:")
# t3.pack(side=LEFT)
# t4= Label(tab2, text="End Date:")
# t4.pack(side=RIGHT)
# t5= Label(tab1, text="Sort Results by:",font=("Arial Bold",15))
# t5.grid(row=2, column=2)
# t6= Label(tab1, text="Search by date range:",font=("Arial Bold",15))
# t6.grid(row=2, column=0)
# t7= Label(tab1, text="Search for specific file & user:",font=("Arial Bold",15))
# t7.grid(row=2, column=1)
#
#  # LABELS / Textboxs
entry_1 = Entry(tab2)
entry_2 = Entry(tab2)
entry_3 = Entry(tab2)
entry_4 = Entry(tab2)
entry_5 = Entry(tab2)
#
# # textboxs
entry_1.grid(row=3,column=0)
entry_2.grid(row=7,column=0)
entry_3.grid(row=3, column=5)
entry_4.grid(row=7, column=5)
# entry_5.grid(row=6, column=0)

# Inspectors
def go_to_one():
    f1.pack()
    f2.pack_forget()
    f3.pack_forget()

def go_to_two():
    f2.pack()
    f1.pack_forget()

def go_to_three():
    f3.pack()
    f1.pack_forget()

master = tk.Tk()
f1 = tk.Frame(master)
f2 = tk.Frame(master)
f3 = tk.Frame(master)
button1 = Button(tab3, text="PREFETCH FILE INSPECTOR", command=go_to_one())
button2 = Button(tab3, text=".LNK FILE INSPECTOR")
button3 = Button(tab3, text="JUMP LIST INSPECTOR")
button4 = Button(tab3, text="INDEX INSPECTOR")
button5 = Button(tab3, text="LOGFILE INSPECTOR")
button6 = Button(tab3, text="SHELLBAG INSPECTOR")
button7 = Button(tab3, text="JOURNAL INSPECTOR")
button8 = Button(tab3, text="TRASH INSPECTOR")
button9 = Button(tab3, text="APP COMPAT CACHE/ SHIMDB INSPECTOR")

button1.grid(row=4, column=2)
button2.grid(row=4, column=3)
button3.grid(row=4, column=4)
button4.grid(row=6, column=2)
button5.grid(row=6, column=3)
button6.grid(row=6, column=4)
button7.grid(row=8, column=2)
button8.grid(row=8, column=3)
button9.grid(row=8, column=4)
# first frame - without f1.pack()
f1 = tk.Frame(master)
l1 = tk.Label(f1, text="Inspectors")
l1.pack()
b1 = tk.Button(f1, text="PREFETCH FILE INSPECTOR", command=go_to_one)
b1.pack()
b2 = tk.Button(f1, text=".LNK FILE INSPECTOR", command=go_to_one)
b2.pack()

# second frame - without f2.pack()
f2 = tk.Frame(master)
l2 = tk.Label(f2, text="PREFETCH FILE INSPECTOR PAGE")
l2.pack()
b2 = tk.Button(f2, text=" Back to Inspectors", command=go_to_one)
b2.pack()

# third frame - without f2.pack()
f3 = tk.Frame(master)
l3 = tk.Label(f3, text=".LNK FILE INSPECTOR PAGE")
l3.pack()
b3 = tk.Button(f3, text=" Back to Inspectors", command=go_to_one)
b3.pack()

# show first frame
f1.pack()



# # Linking Button
# def go_to_first():
#     page3.pack()
#     f2.pack_forget()
#
# def go_to_second():
#     f2.pack()
#     page3.pack_forget()
# def go_to_third():
#     f3.pack()
#     page3.pack_forget()
# root = tk.Tk()
#
# # first frame - without f1.pack()
# page3 = tk.Frame(root)
# l1 = tk.Label(page3, text="Inspectors")
# l1.pack()
# b1 = tk.Button(page3, text="PREFETCH FILE INSPECTOR", command=go_to_second)
# b1.pack()
# b2 = tk.Button(page3, text=".LNK FILE INSPECTOR", command=go_to_third)
# b2.pack()
#
# # second frame - without f2.pack()
# f2 = tk.Frame(root)
# l2 = tk.Label(f2, text="PREFETCH FILE INSPECTOR PAGE")
# l2.pack()
# b2 = tk.Button(f2, text=" Back to Inspectors", command=go_to_first)
# b2.pack()
#
# # third frame - without f2.pack()
# f3 = tk.Frame(root)
# l3 = tk.Label(f3, text=".LNK FILE INSPECTOR PAGE")
# l3.pack()
# b3 = tk.Button(f3, text=" Back to Inspectors", command=go_to_first)
# b3.pack()
#
# # show first frame
# page3.pack()
#

# CHECKBOX

c1 = Checkbutton(tab2, text= "Created")
c2 = Checkbutton(tab2, text= "Modified")
c3 = Checkbutton(tab2, text= "Deleted")
c4 = Checkbutton(tab2, text= "Accessed")
c5 = Checkbutton(tab2, text= "All")

c1.grid(row=3, column=8)
c2.grid(row=4, column=8)
c3.grid(row=5, column=8)
c4.grid(row=6, column=8)
c5.grid(row=7, column=8)

# c1.pack(side=RIGHT)
# c2.pack(side=RIGHT)
# c3.pack(side=RIGHT)
# c4.pack(side=RIGHT)
# c5.pack(side=RIGHT)

# SELECT SYSTEM IMAGE
cx1 = Checkbutton(tab2, text= "Live System")
cx2 = Checkbutton(tab2, text= "System Image")
button12 = Button(tab2, text="Select System Image")

cx1.grid(row=8, column=4)
cx2.grid(row=9, column=4)
button12.grid(row=10,column=4)
tab3.bind('<Return>', (lambda e, b=b: b.invoke()))
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


def clicked():
    print(selected.get())


btn = Button(tab4, text="Submit", command=clicked)

rad1.grid(row=2,column=2)
rad2.grid(row=2,column=3)
rad3.grid(row=2,column=4)
btn.grid(row=2,column=5)

# Calender
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
    btn.grid(row=3,column=2)

    btn = tk.Button(tab2, text="Calendar", command=application)
    btn.grid(row=7,column=2)


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


# Page Transition for Page 3 Inspectors
def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class Calendar(ttk.Frame):
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, year=None, month=None, firstweekday=calendar.MONDAY, locale=None, activebackground='#b1dcfb', activeforeground='black', selectbackground='#003eff', selectforeground='white', command=None, borderwidth=1, relief="solid", on_click_month_button=None):
        """
        WIDGET OPTIONS

            locale, firstweekday, year, month, selectbackground,
            selectforeground, activebackground, activeforeground,
            command, borderwidth, relief, on_click_month_button
        """

        if year is None:
            year = self.datetime.now().year

        if month is None:
            month = self.datetime.now().month

        self._selected_date = None

        self._sel_bg = selectbackground
        self._sel_fg = selectforeground

        self._act_bg = activebackground
        self._act_fg = activeforeground

        self.on_click_month_button = on_click_month_button

        self._selection_is_visible = False
        self._command = command

        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)

        self.bind("<FocusIn>", lambda event :self.event_generate('<<DatePickerFocusIn>>'))
        self.bind("<FocusOut>", lambda event :self.event_generate('<<DatePickerFocusOut>>'))

        self._cal = get_calendar(locale, firstweekday)

        # custom ttk styles
        style = ttk.Style()
        style.layout('L.TButton', (
            [('Button.focus', {'children': [('Button.leftarrow', None)]})]
        ))
        style.layout('R.TButton', (
            [('Button.focus', {'children': [('Button.rightarrow', None)]})]
        ))

        self._font = tkFont.Font()

        self._header_var = StringVar()

        # header frame and its widgets
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._on_press_left_button)
        lbtn.pack(side=LEFT)

        self._header = ttk.Label(hframe, width=15, anchor=CENTER, textvariable=self._header_var)
        self._header.pack(side=LEFT, padx=12)

        rbtn = ttk.Button(hframe, style='R.TButton', command=self._on_press_right_button)
        rbtn.pack(side=LEFT)
        hframe.grid(columnspan=7, pady=4)

        self._day_labels = {}

        days_of_the_week = self._cal.formatweekheader(3).split()

        for i, day_of_the_week in enumerate(days_of_the_week):
            Tkinter.Label(self, text=day_of_the_week, background='grey90').grid(row=1, column=i, sticky= N + E + W +S)

        for i in range(6):
            for j in range(7):
                self._day_labels[i ,j] = label = Tkinter.Label(self, background = "white")

                label.grid(row= i +2, column=j, sticky= N + E + W +S)
                label.bind("<Enter>", lambda event: event.widget.configure(background=self._act_bg, foreground=self._act_fg))
                label.bind("<Leave>", lambda event: event.widget.configure(background="white"))

                label.bind("<1>", self._pressed)

        # adjust its columns width
        font = tkFont.Font()
        maxwidth = max(font.measure(text) for text in days_of_the_week)
        for i in range(7):
            self.grid_columnconfigure(i, minsize=maxwidth, weight=1)

        self._year = None
        self._month = None

        # insert dates in the currently empty calendar
        self._build_calendar(year, month)

    def _build_calendar(self, year, month):
        if not(self._year == year and self._month == month):
            self._year = year
            self._month = month

            # update header text (Month, YEAR)
            header = self._cal.formatmonthname(year, month, 0)
            self._header_var.set(header.title())

            # update calendar shown dates
            cal = self._cal.monthdayscalendar(year, month)

            for i in range(len(cal)):

                week = cal[i]
                fmt_week = [('%02d' % day) if day else '' for day in week]

                for j, day_number in enumerate(fmt_week):
                    self._day_labels[i, j]["text"] = day_number

            if len(cal) < 6:
                for j in range(7):
                    self._day_labels[5, j]["text"] = ""

        if self._selected_date is not None and self._selected_date.year == self._year and self._selected_date.month == self._month:
            self._show_selection()

    def _find_label_coordinates(self, date):
        first_weekday_of_the_month = (date.weekday() - date.day) % 7

        return divmod((first_weekday_of_the_month - self._cal.firstweekday) % 7 + date.day, 7)

    def _show_selection(self):
        """Show a new selection."""

        i, j = self._find_label_coordinates(self._selected_date)

        label = self._day_labels[i, j]

        label.configure(background=self._sel_bg, foreground=self._sel_fg)

        label.unbind("<Enter>")
        label.unbind("<Leave>")

        self._selection_is_visible = True

    def _clear_selection(self):
        """Show a new selection."""
        i, j = self._find_label_coordinates(self._selected_date)

        label = self._day_labels[i, j]
        label.configure(background="white", foreground="black")

        label.bind("<Enter>", lambda event: event.widget.configure(background=self._act_bg, foreground=self._act_fg))
        label.bind("<Leave>", lambda event: event.widget.configure(background="white"))

        self._selection_is_visible = False

    # Callback

    def _pressed(self, evt):
        """Clicked somewhere in the calendar."""

        text = evt.widget["text"]

        if text == "":
            return

        day_number = int(text)

        new_selected_date = datetime.datetime(self._year, self._month, day_number)
        if self._selected_date != new_selected_date:
            if self._selected_date is not None:
                self._clear_selection()

            self._selected_date = new_selected_date

            self._show_selection()

        if self._command:
            self._command(self._selected_date)

    def _on_press_left_button(self):
        self.prev_month()

        if self.on_click_month_button is not None:
            self.on_click_month_button()

    def _on_press_right_button(self):
        self.next_month()

        if self.on_click_month_button is not None:
            self.on_click_month_button()

    def select_prev_day(self):
        """Updated calendar to show the previous day."""
        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date - self.timedelta(days=1)

        self._build_calendar(self._selected_date.year, self._selected_date.month)  # reconstruct calendar

    def select_next_day(self):
        """Update calendar to show the next day."""

        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date + self.timedelta(days=1)

        self._build_calendar(self._selected_date.year, self._selected_date.month)  # reconstruct calendar

    def select_prev_week_day(self):
        """Updated calendar to show the previous week."""
        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date - self.timedelta(days=7)

        self._build_calendar(self._selected_date.year, self._selected_date.month)  # reconstruct calendar

    def select_next_week_day(self):
        """Update calendar to show the next week."""
        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date + self.timedelta(days=7)

        self._build_calendar(self._selected_date.year, self._selected_date.month)  # reconstruct calendar

    def select_current_date(self):
        """Update calendar to current date."""
        if self._selection_is_visible: self._clear_selection()

        self._selected_date = datetime.datetime.now()
        self._build_calendar(self._selected_date.year, self._selected_date.month)

    def prev_month(self):
        """Updated calendar to show the previous week."""
        if self._selection_is_visible: self._clear_selection()

        date = self.datetime(self._year, self._month, 1) - self.timedelta(days=1)
        self._build_calendar(date.year, date.month)  # reconstuct calendar

    def next_month(self):
        """Update calendar to show the next month."""
        if self._selection_is_visible: self._clear_selection()

        date = self.datetime(self._year, self._month, 1) + \
               self.timedelta(days=calendar.monthrange(self._year, self._month)[1] + 1)

        self._build_calendar(date.year, date.month)  # reconstuct calendar

    def prev_year(self):
        """Updated calendar to show the previous year."""

        if self._selection_is_visible: self._clear_selection()

        self._build_calendar(self._year - 1, self._month)  # reconstruct calendar

    def next_year(self):
        """Update calendar to show the next year."""

        if self._selection_is_visible: self._clear_selection()

        self._build_calendar(self._year + 1, self._month)  # reconstruct calendar

    def get_selection(self):
        """Return a datetime representing the current selected date."""
        return self._selected_date

    selection = get_selection

    def set_selection(self, date):
        """Set the selected date."""
        if self._selected_date is not None and self._selected_date != date:
            self._clear_selection()

        self._selected_date = date

        self._build_calendar(date.year, date.month)  # reconstruct calendar


# see this URL for date format information:
#     https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

class Datepicker(ttk.Entry):
    def __init__(self, master, entrywidth=None, entrystyle=None, datevar=None, dateformat="%Y-%m-%d", onselect=None,
                 firstweekday=calendar.MONDAY, locale=None, activebackground='#b1dcfb', activeforeground='black',
                 selectbackground='#003eff', selectforeground='white', borderwidth=1, relief="solid"):

        if datevar is not None:
            self.date_var = datevar
        else:
            self.date_var = Tkinter.StringVar()

        entry_config = {}
        if entrywidth is not None:
            entry_config["width"] = entrywidth

        if entrystyle is not None:
            entry_config["style"] = entrystyle

        ttk.Entry.__init__(self, master, textvariable=self.date_var, **entry_config)

        self.date_format = dateformat

        self._is_calendar_visible = False
        self._on_select_date_command = onselect

        self.calendar_frame = Calendar(self.winfo_toplevel(), firstweekday=firstweekday, locale=locale,
                                       activebackground=activebackground, activeforeground=activeforeground,
                                       selectbackground=selectbackground, selectforeground=selectforeground,
                                       command=self._on_selected_date, on_click_month_button=lambda: self.focus())

        self.bind_all("<1>", self._on_click, "+")

        self.bind("<FocusOut>", lambda event: self._on_entry_focus_out())
        self.bind("<Escape>", lambda event: self.hide_calendar())
        self.calendar_frame.bind("<<DatePickerFocusOut>>", lambda event: self._on_calendar_focus_out())

        # CTRL + PAGE UP: Move to the previous month.
        self.bind("<Control-Prior>", lambda event: self.calendar_frame.prev_month())

        # CTRL + PAGE DOWN: Move to the next month.
        self.bind("<Control-Next>", lambda event: self.calendar_frame.next_month())

        # CTRL + SHIFT + PAGE UP: Move to the previous year.
        self.bind("<Control-Shift-Prior>", lambda event: self.calendar_frame.prev_year())

        # CTRL + SHIFT + PAGE DOWN: Move to the next year.
        self.bind("<Control-Shift-Next>", lambda event: self.calendar_frame.next_year())

        # CTRL + LEFT: Move to the previous day.
        self.bind("<Control-Left>", lambda event: self.calendar_frame.select_prev_day())

        # CTRL + RIGHT: Move to the next day.
        self.bind("<Control-Right>", lambda event: self.calendar_frame.select_next_day())

        # CTRL + UP: Move to the previous week.
        self.bind("<Control-Up>", lambda event: self.calendar_frame.select_prev_week_day())

        # CTRL + DOWN: Move to the next week.
        self.bind("<Control-Down>", lambda event: self.calendar_frame.select_next_week_day())

        # CTRL + END: Close the datepicker and erase the date.
        self.bind("<Control-End>", lambda event: self.erase())

        # CTRL + HOME: Move to the current month.
        self.bind("<Control-Home>", lambda event: self.calendar_frame.select_current_date())

        # CTRL + SPACE: Show date on calendar
        self.bind("<Control-space>", lambda event: self.show_date_on_calendar())

        # CTRL + Return: Set to entry current selection
        self.bind("<Control-Return>", lambda event: self.set_date_from_calendar())

    def set_date_from_calendar(self):
        if self.is_calendar_visible:
            selected_date = self.calendar_frame.selection()

            if selected_date is not None:
                self.date_var.set(selected_date.strftime(self.date_format))

                if self._on_select_date_command is not None:
                    self._on_select_date_command(selected_date)

            self.hide_calendar()

    @property
    def current_text(self):
        return self.date_var.get()

    @current_text.setter
    def current_text(self, text):
        return self.date_var.set(text)

    @property
    def current_date(self):
        try:
            date = datetime.datetime.strptime(self.date_var.get(), self.date_format)
            return date
        except ValueError:
            return None

    @current_date.setter
    def current_date(self, date):
        self.date_var.set(date.strftime(self.date_format))

    @property
    def is_valid_date(self):
        if self.current_date is None:
            return False
        else:
            return True

    def show_date_on_calendar(self):
        date = self.current_date
        if date is not None:
            self.calendar_frame.set_selection(date)

        self.show_calendar()

    def show_calendar(self):
        if not self._is_calendar_visible:
            self.calendar_frame.place(in_=self, relx=0, rely=1)
            self.calendar_frame.lift()

        self._is_calendar_visible = True

    def hide_calendar(self):
        if self._is_calendar_visible:
            self.calendar_frame.place_forget()

        self._is_calendar_visible = False

    def erase(self):
        self.hide_calendar()
        self.date_var.set("")

    @property
    def is_calendar_visible(self):
        return self._is_calendar_visible

    def _on_entry_focus_out(self):
        if not str(self.focus_get()).startswith(str(self.calendar_frame)):
            self.hide_calendar()

    def _on_calendar_focus_out(self):
        if self.focus_get() != self:
            self.hide_calendar()

    def _on_selected_date(self, date):
        self.date_var.set(date.strftime(self.date_format))
        self.hide_calendar()

        if self._on_select_date_command is not None:
            self._on_select_date_command(date)

    def _on_click(self, event):
        str_widget = str(event.widget)

        if str_widget == str(self):
            if not self._is_calendar_visible:
                self.show_date_on_calendar()
        else:
            if not str_widget.startswith(str(self.calendar_frame)) and self._is_calendar_visible:
                self.hide_calendar()


if __name__ == "__main__":
    import sys

    try:
        from Tkinter import Tk, Frame, Label
    except ImportError:
        from tkinter import Tk, Frame, Label

    root = Tk()
    root.geometry("500x600")

    main = Frame()
    main.grid()

    Label(main,tab2,  justify="left", text=__doc__).grid

    Datepicker(main).grid(row=2,column=0)

    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')



root.mainloop()