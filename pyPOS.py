# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v

Point of Sale system for managed retail store
Main file of the system
#test passowrd: Tomate42
'''
import Tkinter as tk#import tkinter Library
import pyPOSLib as lib#import the pyPOs library
#import sys#import sys library

'''
global variable
'''

'''
importing the sys default language
'''
'''
if (lib.language() == "frCA"):#if language is French Canadian
    import language_frCA as text#import the language file
else:
    print "Wrong Language"
    sys.exit(1)   
'''
window = tk.Tk()#create main windows
window.wm_title("pyPOS")#Title of windows
h = window.winfo_screenheight()
w = window.winfo_screenwidth()
    
window.geometry("{0}x{1}+0+0".format(w, h))
window.resizable(0, 0)

mainFrame = tk.Frame(window, borderwidth=1)#genereate the main frame

window.after(500, lib.loginScreen(window, mainFrame))

window.mainloop()

