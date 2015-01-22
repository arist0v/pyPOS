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
            
    except mdb.Error, e:
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
function to start the program
'''

def startProgram():
    global window
    window = tk.Tk()#create main windows
    window.wm_title("pyPOS")#Title of windows
    #global h#global height
    #global w#blobal width
    h = window.winfo_screenheight()
    w = window.winfo_screenwidth()
    
    window.geometry("{0}x{1}+0+0".format(w, h))
    window.resizable(0, 0)


    window.after(500, loginScreen())

    window.mainloop()

'''
function to generate a login screen
'''

def loginScreen():    
    
    try:
        mainFrame.destroy()#try to destroy mainframe(if exist)
    except:
        pass           
        
    global mainFrame  
    mainFrame = tk.Frame(window)#genereate the main frame
    
    global username#set a global username variable
    username = tk.StringVar()
    global password#set a global password variable
    password = tk.StringVar()
        
    messageLabel = tk.Label(mainFrame, text=text.login.message)
    usernameLabel = tk.Label(mainFrame, text=text.login.username)
    usernameField = tk.Entry(mainFrame, textvariable=username, width=30, bg="white")
    usernameField.bind('<Return>', lambda x: auth())#bind Return key when focus on username field
    usernameField.focus()#set focuse on username first
    passwordLabel = tk.Label(mainFrame, text=text.login.password)
    passwordField = tk.Entry(mainFrame, textvariable=password, width=30, show="*", bg="white")
    passwordField.bind('<Return>', lambda x: auth())#bind Return key when focus on password field
    
    loginButton = tk.Button(mainFrame, text=text.login.login, command= lambda: auth())#create login button
    loginButton.bind('<Return>', lambda x: auth())#bind Return key when focus on username field
    quitButton = tk.Button(mainFrame, text=text.login.quit, command=window.quit)#create quit button
    
    
    messageLabel.pack()   
    usernameLabel.pack()
    usernameField.pack()
    passwordLabel.pack()
    passwordField.pack()
    
    loginButton.pack(side="left")
    quitButton.pack(side="right")
    mainFrame.pack(fill="both")
    mainFrame.place(relx=.42, rely=.40)
    
   

'''
function to auth user
'''
def auth():
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
    
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()    
    
    if passCheck(userCheck[0], userPass):#if password is valid
        connectedUser.logged = True#set the connectedUser status to true
        connectedUser.username = user#store username
        connectedUser.level = userCheck[1]#store admin level
        menuScreen()#show menu
    
    

'''
function to compare user provided password versus db password
'''

def passCheck(dbPass, userPass):
    
    if (userPass[:-42] == dbPass[:-42]):#if password minus dynamic salt is identic
        return 1#return true
    else:
        tkm.showwarning("", text.login.invalidPass)#else show warning invalid password

def menuScreen():
    
    if not connectedUser.logged:#if user acces this zone without beeing logged
        loginScreen()#go back to login
        
    try:
        mainFrame.destroy()#reset mainFrame
    except:
        pass   
    
    global mainFrame
    mainFrame = tk.Frame(window)#generate the main frame
    
    global upperFrame
    upperFrame = tk.Frame(mainFrame, borderwidth=5)#genereate the upper frame
    
    global bottomFrame
    bottomFrame = tk.Frame(mainFrame)#genereate the bottom frame
    
    userButton = tk.Button(upperFrame, text=text.menu.user, command= lambda: userManager(), borderwidth=1)
    logoutButton = tk.Button(upperFrame, text=text.menu.logout, command=lambda : sysLogout(), borderwidth=1)

    userButton.grid(row=1, column=1)
    logoutButton.grid(row=1, column=2)
    
    upperFrame.pack(side="top", fill="x")
    bottomFrame.pack(side="bottom", fill="x")
    mainFrame.pack(fill="both")
'''
function to logout from system
'''

def sysLogout():
    connectedUser.level = 0#set user level to 0 
    connectedUser.logged = False#disconnect user
    connectedUser.username = ""#erase username
    loginScreen()#go back to login scren
    
'''
function to access the user management menu
'''
def userManager():
    
    try:
        bottomFrame.destroy()#try to destroy bottomFram if exist
    except:
        pass
    
    try:
        rightSubFrame.destroy()#try to destroy right frame if exist
    except:
        pass
    
    try:
        leftSubFrame.destroy()#try to destroy left fream if exist
    except:
        pass
    
    global bottomFrame  
    bottomFrame = tk.Frame(mainFrame)#recreate a new bottom frame
    
    global leftSubFrame
    leftSubFrame = tk.Frame(bottomFrame, borderwidth=5)
    
    global rightSubFrame
    rightSubFrame = tk.Frame(bottomFrame)
    
    userList = tk.Listbox(leftSubFrame, bg="white")
    userListLabel = tk.Label(leftSubFrame, text=text.userManager.userListLabel)
      
    users = getUserList()
    for user in users:#add each table to list
        userList.insert(0, user[0] +" "+ user[1])
      
    userList.bind('<<ListboxSelect>>', lambda x: userData(userList.get(userList.curselection())))
    
    userListLabel.grid(row=1, column=1)
    userList.grid(row=2, column=1, columnspan=10)
    rightSubFrame.pack(fill="both", pady=25, side="right")
    leftSubFrame.pack(side="left", anchor="w", fill="y")   
    bottomFrame.pack(side="bottom", fill="x")
    
'''
Function to get the list of all user in DB
'''
    
def getUserList():
    
    try:
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor = connection.cursor()
        
        cursor.execute("""SELECT Prenom, Nom FROM Technicien""")#request user information from database
        
        users = cursor.fetchall()# get list of all user      
        
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
        
        return users
    
'''
fonction to print data of selected user
'''
def userData(user):
    
    try:
        rightSubFrame.destroy()#try to destroy right frame if exist
    except:
        pass
    
    global rightSubFrame
    rightSubFrame = tk.Frame(bottomFrame)
    
    firstName = user.split(" ")[0]
    lastName = user.split(" ")[1]
    
    firstNameField = tk.StringVar()
    lastNameField = tk.StringVar()
    
    try:
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor = connection.cursor()
        sql = """SELECT * FROM Technicien WHERE Nom = '{0}' AND Prenom = '{1}'""".format(lastName, firstName)
        
        cursor.execute(sql)#request user information from database
        
        userData = cursor.fetchone()# get list of all user    
      
        
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    firstNameLabel = tk.Label(rightSubFrame, text=text.userManager.firstNameLabel)
    lastNameLabel = tk.Label(rightSubFrame, text=text.userManager.lastNameLabel)
    
    firstNameText = tk.Entry(rightSubFrame, textvariable=firstNameField, bg="white", width=30)
    firstNameText.insert(0, userData[1])
    
    lastNameText = tk.Entry(rightSubFrame, textvariable=lastNameField, bg="white", width=30)
    lastNameText.insert(0, userData[2])
    
    firstNameLabel.grid(row=1, column=1)
    firstNameText.grid(row=1,column=2)
    
    lastNameLabel.grid(row=1, column=3, padx=10)
    lastNameText.grid(row=1, column=4)
    
    rightSubFrame.pack(fill="both", pady=25)
        
        
    
    

    
    