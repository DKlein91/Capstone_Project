import tkinter as tk

def go_to_one():
    f1.pack()
    f2.pack_forget()

def go_to_two():
    f1.pack_forget()
    f2.pack()

def go_to_three():
        f1.pack_forget()
        f2.pack()
        #
        # def go_to_four():
        #     f1.pack()
        #     f2.pack_forget()
        #
        # def go_to_five():
        #     f1.pack_forget()
        #     f2.pack()
        #
        # def go_to_six():
        #     f1.pack_forget()
        #     f2.pack()
        #
        #     def go_to_seven():
        #         f1.pack()
        #         f2.pack_forget()
        #
        #     def go_to_eigth():
        #         f1.pack_forget()
        #         f2.pack()
        #
        #     def go_to_nine():
        #         f1.pack_forget()
        #         f2.pack()


master = tk.Tk()

# first frame - without f1.pack()
f1 = tk.Frame(master)
l1 = tk.Label(f1, text="Inspectors")
l1.pack()
b1 = tk.Button(f1, text="PREFETCH FILE INSPECTOR", command=go_to_two)
b1.pack()
b2 = tk.Button(f1, text=".LNK FILE INSPECTOR", command=go_to_two)
b2.pack()
# b3 = tk.Button(f1, text="JUMP LIST INSPECTOR", command=go_to_four)
# b3.pack()
# b4 = tk.Button(f1, text="INDEX INSPECTOR", command=go_to_five)
# b4.pack()
# b5 = tk.Button(f1, text="LOGFILE INSPECTOR", command=go_to_six)
# b5.pack()
# b6 = tk.Button(f1, text="SHELLBAG INSPECTOR", command=go_to_second)
# b6.pack()
# b7 = tk.Button(f1, text="JOURNAL INSPECTOR", command=go_to_second)
# b7.pack()
# b8 = tk.Button(f1, text="TRASH INSPECTOR", command=go_to_second)
# b8.pack()
# b9 = tk.Button(f1, text="JOURNAL INSPECTOR", command=go_to_second)
# b9.pack()
# b10 = tk.Button(f1, text="APP COMPAT CACHE/ SHIMDB  INSPECTOR", command=go_to_second)
# b10.pack()



# button1 = Button(tab3, text="PREFETCH FILE INSPECTOR")
# button2 = Button(tab3, text=".LNK FILE INSPECTOR")
# button3 = Button(tab3, text="JUMP LIST INSPECTOR")
# button4 = Button(tab3, text="INDEX INSPECTOR")
# button5 = Button(tab3, text="LOGFILE INSPECTOR")
# button6 = Button(tab3, text="SHELLBAG INSPECTOR")
# button7 = Button(tab3, text="JOURNAL INSPECTOR")
# button8 = Button(tab3, text="TRASH INSPECTOR")
# button9 = Button(tab3, text="APP COMPAT CACHE/ SHIMDB INSPECTOR"

# second frame - without f2.pack()
f1 = tk.Frame(master)
l1 = tk.Label(f1, text="Inspectors")
l1.pack()
b1 = tk.Button(f1, text="Trash", command=go_to_one())
f1.pack()

# third frame - without f2.pack()
f2 = tk.Frame(master)

l2 = tk.Label(f2, text="Inspectors")
l2.pack()
b2 = tk.Button(f2, text="Go to Jumplist", command=go_to_one())
b2.pack()
# show first frame
f2.pack()

# # second frame - without f2.pack()
# f2 = tk.Frame(master)
# l2 = tk.Label(f2, text="Inspectors")
# l2.pack()
# b2 = tk.Button(f2, text="Trash", command=go_to_first)
# b2.pack()
#
# # third frame - without f2.pack()
# f3 = tk.Frame(master)
#
# l3 = tk.Label(f2, text="Inspectors")
# l3.pack()
# b3 = tk.Button(f2, text="Go to Jumplist", command=go_to_first)
# b3.pack()
# # show first frame
# f1.pack()
# # f2.pack()

master.mainloop()