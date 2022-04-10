from tkinter import *

master = Tk()

variable = IntVar(master)
variable.set(1) # default value

w = OptionMenu(master, variable, 1, 2, 3,4,5,6)
w.pack()

mainloop()