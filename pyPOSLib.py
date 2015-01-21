# -*- coding: latin1 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v
DB configuration for the program
''''''
from gtk._gtk import SIDE_LEFT
from gtk._gtk import SIDE_RIGHT
Created on 2015-01-20

@author: arist0v
'''
import _mysql#import mysql connector library
import sys#import system database
import dbConfig
import hashlib
import datetime#import time library for dynamic hash generation
import Tkinter as tk#import tkinter Library
import tkMessageBox as tkm

'''
importing the sys default language
'''

'''
#function to get the current sys default language from database
'''
def language():
    try:
        db = _mysql.connect(dbConfig.mysqlServer.server, dbConfig.mysqlServer.user, dbConfig.mysqlServer.password, dbConfig.mysqlServer.database)#connection to mysqldb
        
        db.query("SELECT * FROM sysConfig")#request default system configuration from database
        
        language = db.use_result()#
        
        try:
            data = language.fetch_row()[0][1]#get the language for the result
        except:
            print "no data found"#if failed
    
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if db:
            db.close()
    
    return data#return the language from the database result
'''
import the specied language pack
'''

if (language() == "frCA"):#if language is French Canadian
    import language_frCA as text#import the language file
else:
    print "Wrong Language"
    sys.exit(1)


      
'''
function to encrypt password
'''
def encPassword(clearPass):
    
    staticSalt = "Raxacoricofallapatorius"
    
    hash_object = hashlib.sha512(b'{0}'.format(staticSalt + clearPass))#hash psalt + password
    dynamicSaltBase = datetime.datetime.now().time()
    dynamicHash = hashlib.sha512(b'{0}'.format(dynamicSaltBase))
     
    dynamicSalt = dynamicHash.hexdigest()#get the hash for dynamic salt
    cryptPass = hash_object.hexdigest()#get the hash in hexaor 
    
    cryptPass = cryptPass + dynamicSalt[-42:]
    
    return cryptPass

'''
Function to get default screen size from  Database
'''

def defaultScreenSize():
    try:
        db = _mysql.connect(dbConfig.mysqlServer.server, dbConfig.mysqlServer.user, dbConfig.mysqlServer.password, dbConfig.mysqlServer.database)#connection to mysqldb
        
        db.query("SELECT defaultH, defaultW FROM sysConfig")#request default system configuration from database
        
        size = db.use_result()#
        data = []
        try:
            data = size.fetch_row()[0]#get the height adn width default
            
        except:
            print "no data found"#if failed
    
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if db:
            db.close()
    
    return data#return the language from the database result

'''
function to generate a login screen
'''

def loginScreen(window):
        
    mainFrame = tk.Frame(window, borderwidth=1)
    
    global username
    username = tk.StringVar()
    global password
    password = tk.StringVar()
    global loginErrorMsg
    global messageErrorLabel
    loginErrorMsg = ''
    
    messageLabel = tk.Label(mainFrame, text=text.login.message)
    messageErrorLabel = tk.Label(mainFrame, text=loginErrorMsg)
    usernameLabel = tk.Label(mainFrame, text=text.login.username)
    usernameField = tk.Entry(mainFrame, textvariable=username, width=30)
    passwordLabel = tk.Label(mainFrame, text=text.login.password)
    passwordField = tk.Entry(mainFrame, textvariable=password, width=30, show="*")
    
    
    loginButton = tk.Button(mainFrame, text=text.login.login, command= lambda: auth())#create login button
    quitButton = tk.Button(mainFrame, text=text.login.quit, command=window.quit)#create quit button
    
    messageLabel.pack() 
    messageErrorLabel.pack()  
    usernameLabel.pack()
    usernameField.pack()
    passwordLabel.pack()
    passwordField.pack()
    
    loginButton.pack(side="left")
    quitButton.pack(side="right")
    print loginErrorMsg
    mainFrame.pack()
    mainFrame.place(relx=.42, rely=.40)
   

'''
function to auth user
'''
def auth():
    user = username.get()
    userPass = password.get()
    userPass = encPassword(userPass)
    
    try:
        db = _mysql.connect(dbConfig.mysqlServer.server, dbConfig.mysqlServer.user, dbConfig.mysqlServer.password, dbConfig.mysqlServer.database)#connection to mysqldb
        
        db.query("""SELECT Password FROM Technicien WHERE Username =  '{0}'""".format(user))#request user information from database
        
        size = db.use_result()#
        
        try:
            data = size.fetch_row()[0]#get the height adn width default
            
        except:
            tkm.showwarning("",text.login.invalidUser)#if failed print a message box
            if db:
                db.close()
            return
    
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if db:
            db.close()
    try:
        dbPass = data[0]
    except:
        print ""
    
    if passCheck(dbPass, userPass):
        return 1
    
    

'''
function to compare user provided password versus db password
'''

def passCheck(dbPass, userPass):
    
    if (userPass[:-42] == dbPass[:-42]):#if password minus dynamic salt is identic
        return 1#return true
    else:
        tkm.showwarning("", text.login.invalidPass)#else show warning invalid password


    
    