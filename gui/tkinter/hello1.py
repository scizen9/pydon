# File: hello1.py

from Tkinter import *

__version__ = "$Id: hello1.py,v 1.1 2011/06/22 22:09:09 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/gui/tkinter/hello1.py,v $

root = Tk()

w = Label(root, text="Hello, world!")
w.pack()

root.mainloop()
