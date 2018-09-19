# File: hello2.py

from Tkinter import *

__version__ = "$Id: hello2.py,v 1.2 2011/07/01 00:04:38 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/gui/tkinter/hello2.py,v $

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi there, everyone. I'm output!"

root = Tk()

app = App(root)

root.mainloop()
