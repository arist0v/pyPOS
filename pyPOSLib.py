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

import MySQLdb as mdb#import mysqldb library
import sys#import system database
import dbConfig#import personnal lib dbconfig
import hashlib#import hash library
import datetime#import time library for dynamic hash generation
import Tkinter as tk#import tkinter Library
import tkMessageBox as tkm#import tk message box


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
        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)
        
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM sysConfig")
                
        language = cursor.fetchall()[0][1]
            
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    return language#return the language from the database result
'''
import the specied language pack

add new language by adding similar elif
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
        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute("""SELECT Password, levelID FROM Technicien WHERE Username =  '{0}'""".format(user))#request user information from database
        
        userCheck = cursor.fetchone()#
        
        if (userCheck == None):
            tkm.showwarning("",text.login.invalidUser)#if no user found print warning
            return
    
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()    
    
    if passCheck(userCheck[0], userPass):#if password is valid
        connectedUser.logged = True#set the connectedUser status to true
        connectedUser.username = user#store username
        connectedUser.level = userCheck[1]#store admin level
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
    
    mainFrame = tk.Frame(window, borderwidth=1)#generate the main frame
    upperFrame = tk.Frame(mainFrame, borderwidth=1)#genereate the upper frame
    bottomFrame = tk.Frame(mainFrame, borderwidth=1)#genereate the bottom frame
    
    userButton = tk.Button(upperFrame, text=text.menu.user, command= lambda: userManager(window, bottomFrame, mainFrame))
    logoutButton = tk.Button(upperFrame, text=text.menu.logout, command=lambda : sysLogout(window, mainFrame))

    userButton.grid(row=1, column=1)
    logoutButton.grid(row=1, column=2)
    
    upperFrame.pack()
    bottomFrame.pack()
    mainFrame.pack()
'''
function to logout from system
'''

def sysLogout(window, mainFrame):
    connectedUser.level = 0#set user level to 0 
    connectedUser.logged = False#disconnect user
    connectedUser.username = ""#erase username
    loginScreen(window,mainFrame)#go back to login scren
    
'''
function to access the user management menu
'''
def userManager(window, bottomFrame, mainFrame):
    bottomFrame.destroy()#destroy the bottom frame
    
    bottomFrame = tk.Frame(mainFrame, borderwidth=1)#recreate a new bottom frame
    
    userList = tk.Listbox(bottomFrame)
    
    userList.grid(row=1, column=1, columnspan=10, sticky="W")
    
    users = getUserList()
    for user in users:
        userList.insert(1, user[0] +" "+ user[1])
        
    bottomFrame.pack()
    
'''
Function to get the list of all user in DB
'''
    
def getUserList():
    
    data = []#empty table to store user list
    
    try:
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor = connection.cursor()
        
        cursor.execute("""SELECT Prenom, Nom FROM Technicien""")#request user information from database
        
        users = cursor.fetchall()# get list of all user      
        
    except _mysql.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
        
        return users
    
    
    
    

    
    