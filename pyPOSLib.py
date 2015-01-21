# -*- coding: utf-8 -*-
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
import tkMessageBox as tkm#import tk message box
from PIL import Image #import image library
import ImageTk# as tki #import image tk library

'''
importing the sys default language
'''

class loginInfo:
    '''Class who contain all login info'''
    def __init__(self):
        
        self.logged = False
        self.username = ""
        self.level = 0
        
connectedUser = loginInfo()

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

def loginScreen(window, mainFrame):
    mainFrame.destroy()  
    mainFrame = tk.Frame(window, borderwidth=1)#genereate the main frame
    
    global username#set a global username variable
    username = tk.StringVar()
    global password#set a global password variable
    password = tk.StringVar()
        
    messageLabel = tk.Label(mainFrame, text=text.login.message)
    usernameLabel = tk.Label(mainFrame, text=text.login.username)
    usernameField = tk.Entry(mainFrame, textvariable=username, width=30)
    usernameField.bind('<Return>', lambda x: auth(window, mainFrame))#bind Return key when focus on username field
    usernameField.focus()#set focuse on username first
    passwordLabel = tk.Label(mainFrame, text=text.login.password)
    passwordField = tk.Entry(mainFrame, textvariable=password, width=30, show="*")
    passwordField.bind('<Return>', lambda x: auth(window, mainFrame))#bind Return key when focus on password field
    
    loginButton = tk.Button(mainFrame, text=text.login.login, command= lambda: auth(window, mainFrame))#create login button
    loginButton.bind('<Return>', lambda x: auth(window, mainFrame))#bind Return key when focus on username field
    quitButton = tk.Button(mainFrame, text=text.login.quit, command=window.quit)#create quit button
    
    
    messageLabel.pack()   
    usernameLabel.pack()
    usernameField.pack()
    passwordLabel.pack()
    passwordField.pack()
    
    loginButton.pack(side="left")
    quitButton.pack(side="right")
    mainFrame.pack()
    mainFrame.place(relx=.42, rely=.40)
    
   

'''
function to auth user
'''
def auth(window, mainFrame):
    user = username.get()#get the global username from field
    userPass = password.get()#get the global password from field
    userPass = encPassword(userPass)#convert password to hash
    
    try:
        db = _mysql.connect(dbConfig.mysqlServer.server, dbConfig.mysqlServer.user, dbConfig.mysqlServer.password, dbConfig.mysqlServer.database)#connection to mysqldb
        
        db.query("""SELECT Password, levelID FROM Technicien WHERE Username =  '{0}'""".format(user))#request user information from database
        
        size = db.use_result()#
        
        try:
            data = size.fetch_row()[0]
            
        except:
            tkm.showwarning("",text.login.invalidUser)#if no user found print warning
            return
    
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if db:
            db.close()    
    
    if passCheck(data[0], userPass):#if password is valid
        connectedUser.logged = True#set the connectedUser status to true
        connectedUser.username = user#store username
        connectedUser.level = data[1]#store admin level
        menuScreen(window, mainFrame)#show menu
    
    

'''
function to compare user provided password versus db password
'''

def passCheck(dbPass, userPass):
    
    if (userPass[:-42] == dbPass[:-42]):#if password minus dynamic salt is identic
        return 1#return true
    else:
        tkm.showwarning("", text.login.invalidPass)#else show warning invalid password

def menuScreen(window, mainFrame):
    
    if not connectedUser.logged:#if user acces this zone without beeing logged
        loginScreen(window, mainFrame)#go back to login
        
    mainFrame.destroy()#reset the mainFrame for new use
    
    mainFrame = tk.Frame(window, borderwidth=1)#genereate the main frame

    logoutButton = tk.Button(mainFrame, text=text.menu.logout, command=lambda : sysLogout(window, mainFrame))

    logoutButton.pack()
    mainFrame.pack()
'''
function to logout from system
'''

def sysLogout(window, mainFrame):
    connectedUser.level = 0#set user level to 0 
    connectedUser.logged = False#disconnect user
    connectedUser.username = ""#erase username
    loginScreen(window,mainFrame)#go back to login scren
    
    

    
    