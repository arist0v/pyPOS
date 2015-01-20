# -*- coding: latin1 -*-
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
import sys#import sys library

'''
importing the sys default language
'''
if (lib.language() == "frCA"):#if language is French Canadian
    import language_frCA as text#import the language file
else:
    print "Wrong Language"
    sys.exit(1)

#lib.importLanguage(lib.language())#import the correct language file library

lib.loginScreen()
