#!/usr/bin/env python
import wx

__version__ = "$Id: hello.py,v 1.1 2011/06/22 22:10:09 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/gui/wx/hello.py,v $

app = wx.App(False)                                                # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)                                                     # Show the frame.
app.MainLoop()
