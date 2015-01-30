#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2015-01-20

@author: arist0v

Point of Sale system for managed retail store
Main file of the system
#test passowrd: Tomate42
'''

import MySQLdb as mdb#import mysqldb library
import sys#import system database
import dbConfig#import personnal lib dbconfig
import hashlib#import hash library
import datetime#import time library for dynamic hash generation
import Tkinter as tk#import tkinter Library
import tkMessageBox as tkm#import tk message box
import os#import the OS function
import time#import the time module
import locale#import the local module

global version#create global var for version number
version = "0.1"#current version

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
import the language pack specified in the DB
'''

langFile = "Languages.language_" + language()
__import__(langFile)
text = sys.modules[langFile]
     
'''
function to encrypt password
'''
def encPassword(clearPass):
    
    staticSalt = "Raxacoricofallapatorius"
    clearPass = clearPass.encode("utf-8")
    
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
    window.wm_title(text.mainText.mainWindowTitle + " - " + version)#Title of windows
    global h#global height
    global w#blobal width
    h = window.winfo_screenheight()
    w = window.winfo_screenwidth()
    window.geometry("{0}x{1}+0+0".format(w, h))#start maximized
    
    #window.attributes('-fullscreen', True)#start in full screen mode
    #window.resizable(0, 0)#disable resize


    window.after(1, loginScreen())

    window.mainloop()
    
'''
function to show the licence in a popup
'''
def showLicence():
    licence = tk.Toplevel(window)    
    licence.title(text.licence.title)
    
    scroll = tk.Scrollbar(licence)
    scroll.pack( side = "right", fill="y" )
    
    quitButton = tk.Button(licence, text="OK", command=lambda :licence.destroy())
    
    licenceText = tk.Text(licence, yscrollcommand=scroll.set, bg="white")
    
    licenceContent = open("LICENSE", "r")
    
    licenceText.insert("insert", licenceContent.read())
    
    licenceText.configure(state="disabled")
    
    scroll.configure(command = licenceText.yview)    
    
    licenceText.pack()
    quitButton.pack()     

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
    
    global formFrame
    formFrame = tk.Frame(mainFrame)
    
    global buttonFrame
    buttonFrame = tk.Frame(formFrame)
       
    global username#set a global username variable
    username = tk.StringVar()
    global password#set a global password variable
    password = tk.StringVar()
        
    messageLabel = tk.Label(formFrame, text=text.login.message)
    usernameLabel = tk.Label(formFrame, text=text.login.username)
    usernameField = tk.Entry(formFrame, textvariable=username, width=30, bg="white")
    usernameField.bind('<Return>', lambda x: auth())#bind Return key when focus on username field
    usernameField.bind('<KP_Enter>', lambda x: auth())#numpad enter
    usernameField.bind('<Key-Escape>', lambda x: window.quit())
    usernameField.focus()#set focuse on username first
    passwordLabel = tk.Label(formFrame, text=text.login.password)
    passwordField = tk.Entry(formFrame, textvariable=password, width=30, show="*", bg="white")
    passwordField.bind('<Return>', lambda x: auth())#bind Return key when focus on password field
    passwordField.bind('<KP_Enter>', lambda x: auth())#numpad enter
    passwordField.bind('<Escape>',lambda x: window.quit())
    
    loginButton = tk.Button(buttonFrame, text=text.login.login, command= lambda: auth(), width=10)#create login button
    loginButton.bind('<Return>', lambda x: auth())#bind Return key when focus on username field
    loginButton.bind('<KP_Enter>', lambda x: auth())#numpad enter
    loginButton.bind('<Escape>',lambda x: window.quit())
    quitButton = tk.Button(buttonFrame, text=text.login.quit, command=window.quit, width=10)#create quit button
    licenceLabel = tk.Label(formFrame, text=text.login.licence)
    licenceLabel.bind("<Button-1>",lambda x: showLicence())
    
    
    messageLabel.pack()
    usernameLabel.pack()
    usernameField.pack()
    passwordLabel.pack()
    passwordField.pack()
    
    loginButton.grid(sticky="w", row=1, column=1, pady=5)
    quitButton.grid(sticky="e", row=1, column=2, pady=5)
    buttonFrame.pack()
    licenceLabel.pack()
    formFrame.pack(anchor="center", expand=True)
    mainFrame.pack(fill="both", expand=True)
    
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
            tkm.showerror("",text.login.invalidUser)#if no user found print warning
            loginScreen()
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
    else:
        loginScreen()
    

'''
function to compare user provided password versus db password
'''

def passCheck(dbPass, userPass):
    
    if (userPass[:-42] == dbPass[:-42]):#if password minus dynamic salt is identic
        return 1#return true
    else:
        tkm.showerror("", text.login.invalidPass)#else show warning invalid password

'''
function to show the upper menu bar
'''
def menuScreen():
       
    state="disabled"
    
    if not connectedUser.logged:#if user acces this zone without beeing logged
        loginScreen()#go back to login
    
    if (connectedUser.level == 3):#if user is admin
        state="normal"
    try:
        mainFrame.destroy()#reset mainFrame
    except:
        pass   
    
    global mainFrame
    mainFrame = tk.Frame(window)#generate the main frame

    global upperFrame
    upperFrame = tk.Frame(mainFrame, borderwidth=5)#genereate the upper frame

    global menuFrame
    menuFrame = tk.Frame(upperFrame)
    
    global bottomFrame
    bottomFrame = tk.Frame(mainFrame)#genereate the bottom frame
    
    userButton = tk.Button(menuFrame,width=10, text=text.menu.user, command= lambda: userManager(), borderwidth=1)
    configButton = tk.Button(menuFrame,width=10, text=text.menu.config, command=lambda: sysConfig())
    configButton.config(state=state)
    logoutButton = tk.Button(menuFrame,width=10, text=text.menu.logout, command=lambda : sysLogout(), borderwidth=1)
    userLoggedLabel = tk.Label(upperFrame, text=text.menu.userLogged + connectedUser.username)
    
    '''
    sub-function to get and update clock on upper frame
    '''
    
    def clock():
        locale.setlocale(locale.LC_ALL, text.menu.locale)#set the locale
        current = time.strftime("%A, %d %B %Y, %H:%M:%S")#get current time
        clockLabel.configure(text=current)#update labale with current time
        upperFrame.after(500, clock)#do it every 500 milisec.
        
    clockLabel = tk.Label(upperFrame, text="")
    clock()
    
    #userLoggedLabel.grid(row=1, column=1, columnspan=3, sticky="nsew")
    userLoggedLabel.pack()
    #clockLabel.grid(row=2, column=1, columnspan=3, sticky="nsew")
    clockLabel.pack()
    userButton.grid(row=1, column=1, padx=(5,0), sticky="nsew")
    #userButton.pack(side="left", padx=2)
    configButton.grid(row=1, column=2, padx=(5,0), sticky="nsew")
    #configButton.pack(side="left", padx=2)
    logoutButton.grid(row=1, column=3, padx=(5,0), sticky="nsew")
    #logoutButton.pack(side="left", padx=2)
    
    upperFrame.pack(side="top")
    menuFrame.pack()
    bottomFrame.pack(side="bottom", fill="both", expand=True)
    mainFrame.pack(fill="both", expand=True)



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
    
    state="disabled"
    
    if (connectedUser.level == 3):#if user is admin
        state="normal"#he can add new user 
    
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
    
    addUserButton = tk.Button(leftSubFrame, text=text.userManager.addUserButton, command=lambda: newUser())
    addUserButton.configure(state=state)
      
    users = getUserList()
    for user in users:#add each table to list
        userList.insert(0, user[0] +" "+ user[1])
      
    userList.bind('<<ListboxSelect>>', lambda x: userData(userList.get(userList.curselection())))
    
    userListLabel.grid(row=1, column=1)
    userList.grid(row=2, column=1, columnspan=1)
    addUserButton.grid(row=3, column=1, columnspan=1, pady=(5,0))
    leftSubFrame.pack(side="left", fill="both", expand=True)
    rightSubFrame.pack(fill="both",side="right", expand=True)
    
       

    bottomFrame.pack(side="bottom", fill="y",anchor="w", expand=True)
    
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
    
    state="disabled"#defautl state for edit user enabled on manager or itself
    state2="disabled"#default state to edit user enablaed on adminstrator or itself
    state3="disabled"#default state to edit user on adminstrator only
    state4="disabled"#default state to allow delete user on administrato when not itself
      
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
    emailField = tk.StringVar()
    levelField = tk.StringVar()
    #oldPassField = tk.StringVar()
    
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
            
    if (connectedUser.level == 2 or connectedUser.username == userData[4]):#if user is manager or itself
        state="normal"
    
    if (connectedUser.level == 3 or connectedUser.username == userData[4]):#if user is admin or itself
        state="normal"
        state2="normal"
        
    if (connectedUser.level == 3):#if user is Administrator
        state3="normal"
        
    if (connectedUser.level == 3 and not connectedUser.username == userData[4]):#if user is Administrator and is not itself for delete command
        state4="normal"#enable delete button
            
    firstNameLabel = tk.Label(rightSubFrame, text=text.userManager.firstNameLabel)
    lastNameLabel = tk.Label(rightSubFrame, text=text.userManager.lastNameLabel)
    emailLabel = tk.Label(rightSubFrame, text=text.userManager.emailLabel)
    levelLabel = tk.Label(rightSubFrame, text=text.userManager.levelLabel)
    
    firstNameText = tk.Entry(rightSubFrame, textvariable=firstNameField, bg="white", width=30)
    firstNameText.insert(0, userData[1])
    firstNameText.configure(state=state2)
    
    lastNameText = tk.Entry(rightSubFrame, textvariable=lastNameField, bg="white", width=30)
    lastNameText.insert(0, userData[2])
    lastNameText.configure(state=state2)
    
    emailText = tk.Entry(rightSubFrame, textvariable=emailField, bg="white", width=30)
    emailText.insert(0, userData[3])
    emailText.configure(state=state2)
    
    levelMenu = tk.OptionMenu(rightSubFrame, levelField, text.userManager.levelUser, text.userManager.levelManager, text.userManager.levelAdmin)
    levelMenu["menu"].config(bg="white")
    levelMenu.configure(width=26, bg="white")
    levelMenu.configure(state=state3)
    
    changePassButton = tk.Button(rightSubFrame, text=text.userManager.changePassButton, command= lambda: changeUserPass(userData[4]))
    changePassButton.config(state=state)
    
    deleteUserButton = tk.Button(rightSubFrame, text=text.userManager.deleteUserButton, command=lambda: deleteUser(userData[4], userData[1], userData[2]))
    deleteUserButton.configure(state=state4)
    
    saveButton = tk.Button(rightSubFrame, text=text.userManager.saveButton, command = lambda: saveUserData(firstNameField.get(), lastNameField.get(), emailField.get(), levelField.get(), userData[4]))
    saveButton.config(state=state2)
            
    if (userData[6] == 2):
        levelField.set(text.userManager.levelManager)
    elif (userData[6] == 3):
        levelField.set(text.userManager.levelAdmin)
    else:
        levelField.set(text.userManager.levelUser)      
        
    firstNameLabel.grid(row=1, column=1)
    firstNameText.grid(row=1,column=2)
    
    lastNameLabel.grid(row=1, column=3, padx=10)
    lastNameText.grid(row=1, column=4)
    
    emailLabel.grid(row=2, column=1, pady=(20,0))
    emailText.grid(row=2, column=2, pady=(20,0))
    
    levelLabel.grid(row=2, column=3, pady=(20,0))
    levelMenu.grid(row=2, column=4, pady=(20,0))
    
    changePassButton.grid(row=3, column=1, columnspan=1, sticky="w", pady=(20,0))
    deleteUserButton.grid(row=3, column=2, columnspan=2, pady=(20,0))
    saveButton.grid(row=3, column=4, columnspan=1, sticky="e", pady=(20,0))
    
    rightSubFrame.pack(fill="both", expand=True, anchor="w")
    
'''
function to delete a user
'''
def deleteUser(username, firstName, LastName):
    
    confirm = tkm.askquestion(text.deleteUser.windowTitle, text.deleteUser.deleteConfrim + username)
    if (confirm == 'yes'):
        sql = """DELETE FROM Technicien WHERE Username = '{0}'""".format(username)

        try:
            connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
            cursor = connection.cursor()
        
            cursor.execute(sql)#send update to database
        
            connection.commit()

        except mdb.Error, e:
            print "Error: {0} {1}".format(e.args[0], e.args[1])
            sys.exit(1)
            
        finally:
            if connection:
                connection.close()
        
        tkm.showinfo(text.deleteUser.windowTitle, text.deleteUser.confirm + username + text.deleteUser.confirm2)
        userManager()
        
    else:
        userData(firstName + " " + LastName)
            
'''
function to change save to userData
'''
def saveUserData(firstName, lastName, email, adminLevel, username):
    
    if (adminLevel == text.userManager.levelAdmin):#convert adminLevel to equivalent ID
        levelID = 3
    elif (adminLevel.encode("utf-8") == text.userManager.levelManager):
        levelID = 2
    else:
        levelID = 1
        
    sql="""UPDATE Technicien SET Prenom='{0}',Nom='{1}', Email='{2}', levelID='{3}' WHERE Username='{4}'""".format(firstName.encode("utf-8"), lastName.encode("utf-8"), email.encode("utf-8"), levelID, username.encode("utf-8"))
    
    try:
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor = connection.cursor()
        
        cursor.execute(sql)#send update to database
        
        connection.commit()

    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    tkm.showinfo("", text.userManager.savePopUp)
    
'''
function to change the user password
'''
   
def changeUserPass(userName):
    
    global changePassScreen
    
    changePassScreen = tk.Toplevel(window)#create a popup window
    changePassScreen.title(text.changePassword.windowTitle)
       
    varOldPass = tk.StringVar()
    varNewPass = tk.StringVar()
    varConfirmPass = tk.StringVar()
    
    changePassLabel = tk.Label(changePassScreen, text=text.changePassword.instructionLabel, wraplength=300)#label containing instruction
    oldPassLabel = tk.Label(changePassScreen, text=text.changePassword.oldPass)#old pass label
    newPassLabel = tk.Label(changePassScreen, text=text.changePassword.newPass)#new pass label
    confirmPassLabel = tk.Label(changePassScreen, text=text.changePassword.confirmPass)#confirm password label
    
    oldPassEntry = tk.Entry(changePassScreen, bg="white", width=20, show="*", textvariable=varOldPass)
    oldPassEntry.focus()
    newPassEntry = tk.Entry(changePassScreen, bg="white", width=20, show="*", textvariable=varNewPass)
    confirmPassEntry = tk.Entry(changePassScreen, bg="white", width=20, show="*", textvariable=varConfirmPass)
    
    changeButton = tk.Button(changePassScreen, text=text.changePassword.changeButton, command=lambda: saveNewPass(userName, connectedUser.username, varOldPass.get(), varNewPass.get(), varConfirmPass.get()))
    cancelButton = tk.Button(changePassScreen, text=text.changePassword.cancelButton, command=lambda : changePassScreen.destroy())
    
    changePassLabel.grid(row=1, column=1, columnspan=2)
    
    oldPassLabel.grid(row=2, column=1, pady=(20,0), padx=(5,0))
    oldPassEntry.grid(row=2, column=2, pady=(20,0), padx=5)
    
    newPassLabel.grid(row=3, column=1, pady=(20,0), padx=(5,0))
    newPassEntry.grid(row=3, column=2, pady=(20,0), padx=5)
    
    confirmPassLabel.grid(row=4, column=1, pady=(20,0), padx=(5,0))
    confirmPassEntry.grid(row=4, column=2, pady=(20,0), padx=5)
    
    changeButton.grid(row=5, column=1, pady=(20,0))
    cancelButton.grid(row=5, column=2, pady=(20,0))
    
'''
function to save the new password
'''
def saveNewPass(userName, connectedUser, oldPass, newPass, confirmPass):
    
    warningMessage = ""
    
    userPass = encPassword(oldPass)
    
    #intialize password verification bool
    passLower=0
    passUpper=0
    passDigit=0
    passLen=0
    goodConfirm=0
    
    try:
        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute("""SELECT Password FROM Technicien WHERE Username =  '{0}'""".format(connectedUser))#request user information from database
        
        userCheck = cursor.fetchone()#
           
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    if passCheck(userCheck[0], userPass):#if password is valid
        oldPassGood = 1
        
        if (newPass == confirmPass):#if the new pass and confirmation are the same
            goodConfirm = 1
        
            if passContainLower(newPass):#if password contain lower case
                passLower= 1
            else:
                warningMessage = warningMessage + text.changePassword.onlyUpper + "\n"
        
            if passContainUpper(newPass):#if password contain upper case
                passUpper= 1
            else:
                warningMessage = warningMessage + text.changePassword.onlyLower + "\n"
        
            if passContainDigit(newPass):#if password contain digit
                passDigit = 1
            else:
                warningMessage = warningMessage + text.changePassword.noDigit + "\n"
            
            if (len(newPass) >=  6):  
                passLen=1
            else:
                warningMessage = warningMessage + text.changePassword.passShort + "\n"
        
        else:
            goodConfirm = 0
            warningMessage = warningMessage + text.changePassword.badConfirm + "\n"
        
    else:
        oldPassGood = 0 
        
    if oldPassGood and passLower and passUpper and passDigit and goodConfirm and passLen:
        sql = """UPDATE Technicien SET Password = '{0}' WHERE Username = '{1}'""".format(encPassword(newPass), userName)#build sql request
        
        try:        
            connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
            cursor= connection.cursor()
        
            cursor.execute(sql)#request to save user password
            
            connection.commit()#commit change
           
        except mdb.Error, e:
            print "Error: {0} {1}".format(e.args[0], e.args[1])
            sys.exit(1)
            
        finally:
            if connection:
                connection.close()
        
        changePassScreen.destroy()
    else:
        if oldPassGood:#if message is not from old password wrong
            tkm.showerror(text.changePassword.errorTitle, warningMessage)
        changePassScreen.destroy()
        
'''
function to look if password contain lowerCase
'''
def passContainLower(newPass):
    for char in newPass:
        if char.islower():
            return 1
    else:
        return 0
    
'''
function to look if password contain upperCase
'''
    
def passContainUpper(newPass):
    for char in newPass:
        if char.isupper():
            return 1
    else:
        return 0
'''
function to look if password contain digit
'''
def passContainDigit(newPass):
    for char in newPass:
        if char.isdigit():
            return 1
    else:
        return 0
    
'''
function to add a new user
'''

def newUser():
    
    try:
        rightSubFrame.destroy()#try to destroy right frame if exist
    except:
        pass
    
    global rightSubFrame
    rightSubFrame = tk.Frame(bottomFrame)
    
    firstNameField = tk.StringVar()
    lastNameField = tk.StringVar()
    emailField = tk.StringVar()
    levelField = tk.StringVar()
    passField = tk.StringVar()
    confirmPassField = tk.StringVar()
    usernameField = tk.StringVar()
    
    firstNameLabel = tk.Label(rightSubFrame, text=text.newUser.firstNameLabel)
    lastNameLabel = tk.Label(rightSubFrame, text=text.newUser.lastNameLabel)
    emailLabel = tk.Label(rightSubFrame, text=text.newUser.emailLabel)
    levelLabel = tk.Label(rightSubFrame, text=text.newUser.levelLabel)
    passwordLabel = tk.Label(rightSubFrame, text=text.newUser.passwordLabel)
    confirmPassLabel = tk.Label(rightSubFrame, text=text.newUser.confirmPassLabel)
    usernameLabel = tk.Label(rightSubFrame, text=text.newUser.usernameLabel)
    
    firstNameText = tk.Entry(rightSubFrame, textvariable=firstNameField, bg="white", width=30)
    firstNameText.focus()    
    lastNameText = tk.Entry(rightSubFrame, textvariable=lastNameField, bg="white", width=30)    
    emailText = tk.Entry(rightSubFrame, textvariable=emailField, bg="white", width=30)

    levelMenu = tk.OptionMenu(rightSubFrame, levelField, text.newUser.levelUser, text.newUser.levelManager, text.newUser.levelAdmin)
    levelMenu["menu"].config(bg="white")
    levelMenu.configure(width=26, bg="white")
    levelField.set(text.newUser.levelUser)
    
    passwordText = tk.Entry(rightSubFrame, textvariable=passField, bg="white", width=30, show="*")
    confPassText = tk.Entry(rightSubFrame, textvariable=confirmPassField, bg="white", width=30, show="*")    
    
    usernameText = tk.Entry(rightSubFrame, textvariable=usernameField, bg="white", width=30)
    
    saveButton = tk.Button(rightSubFrame, text=text.newUser.saveButton, command=lambda: saveNewUser(firstNameField.get().encode("utf-8"), lastNameField.get().encode("utf-8"), emailField.get(), levelField.get(), usernameField.get().encode("utf-8"), passField.get(), confirmPassField.get()))
    
    firstNameLabel.grid(row=1, column=1)
    firstNameText.grid(row=1,column=2)
    
    lastNameLabel.grid(row=1, column=3, padx=10)
    lastNameText.grid(row=1, column=4)
    
    emailLabel.grid(row=2, column=1, pady=(20,0))
    emailText.grid(row=2, column=2, pady=(20,0))
    
    levelLabel.grid(row=2, column=3, pady=(20,0))
    levelMenu.grid(row=2, column=4, pady=(20,0))
    
    passwordLabel.grid(row=3, column=1, pady=(20,0))
    passwordText.grid(row=3, column=2, pady=(20,0))
    confirmPassLabel.grid(row=3, column=3, pady=(20,0))
    confPassText.grid(row=3, column=4, pady=(20,0))    

    usernameLabel.grid(row=4, column=1, pady=(20,0))
    usernameText.grid(row=4, column=2, pady=(20,0))
    saveButton.grid(row=4, column=3, columnspan=2, pady=(20,0))
    
    rightSubFrame.pack(fill="both", pady=25)
    
'''
function to commit the new user
'''
def saveNewUser(firstName, lastName, email, adminLevel, username, password, confirmPassword):
    
    warningMessage = ""
    
    passLower=0
    passUpper=0
    passDigit=0
    passLen=0
    passConfirm=0
    checkPassword=0
    checkFirstName=0
    checkLastName=0
    checkUsername=0
    
    if (password == confirmPassword):
        passConfirm=1
        if passContainLower(password):#if password contain lower case
            passLower= 1
        else:
            warningMessage = warningMessage + text.changePassword.onlyUpper + "\n"
        
        if passContainUpper(password):#if password contain upper case
            passUpper= 1
        else:
            warningMessage = warningMessage + text.changePassword.onlyLower + "\n"
        
        if passContainDigit(password):#if password contain digit
            passDigit = 1
        else:
            warningMessage = warningMessage + text.changePassword.noDigit + "\n"
            
        if (len(password) >=  6):  
            passLen=1
        else:
            warningMessage = warningMessage + text.changePassword.passShort + "\n"
        
    else:
        warningMessage = text.newUser.wrongConfirm
    
    if passConfirm and passLower and passUpper and passDigit and passLen:
        checkPassword = 1
        
        if (firstName == ""):
            warningMessage = warningMessage + text.newUser.noFirstName + "\n"
        else:
            checkFirstName = 1
        if (lastName == ""):
            warningMessage = warningMessage + text.newUser.noLastName + "\n"
        else:
            checkLastName = 1
        if (username == ""):
            warningMessage = warningMessage + text.newUser.noUsername + "\n"
        else:
            checkUsername = 1
        if checkFirstName and checkLastName and checkUsername:
            
            if (adminLevel == text.userManager.levelAdmin):#convert adminLevel to equivalent ID
                adminLevel = 3
            elif (adminLevel.encode("utf-8") == text.userManager.levelManager):
                adminLevel = 2
            else:
                adminLevel = 1
            
            sql = """INSERT INTO Technicien(Prenom, Nom, Email, Username, Password, levelID) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(firstName, lastName, email, username, encPassword(password), adminLevel)
            
            try:        
                connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
                cursor= connection.cursor()
        
                cursor.execute(sql)#request to save user password
            
                connection.commit()#commit new user
           
            except mdb.Error, e:
                print "Error: {0} {1}".format(e.args[0], e.args[1])
                sys.exit(1)
            
            finally:
                if connection:
                    connection.close()
                tkm.showinfo(text.newUser.userAddedTitle, text.newUser.userAdded)
                userManager()                        
        else:
            tkm.showerror(text.newUser.errorTitle, warningMessage)
    else:                
        tkm.showerror(text.newUser.errorTitle, warningMessage)  
        
'''
function to open the system configuration
'''
def sysConfig():
    
    state="disabled"
    state2="disabled"
    
    if (connectedUser.level == 3):#if user is admin
        state="normal"#enable admin only config
        
    if (connectedUser.level == 2 or connectedUser.level == 3):#if user is manager or admin
        state2="normal"#enable manager nor admin config
    
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
    
    languageButton = tk.Button(leftSubFrame, text=text.sysConfig.menuLanguage, width=15, command= lambda: langConfig())
    languageButton.config(state=state2)
    storeInfoButton = tk.Button(leftSubFrame, text=text.sysConfig.menuStoreInfo, width=15, command= lambda: storeInfo())
    storeInfoButton.config(state=state)
    databaseButton = tk.Button(leftSubFrame, text=text.sysConfig.menuDatabase, width=15)
    databaseButton.config(state=state)
    taxeButton = tk.Button(leftSubFrame, text=text.sysConfig.menuTaxe, width=15, command= lambda: taxeInfo())
    taxeButton.config(state=state2)
    taxeGroupButton = tk.Button(leftSubFrame, text=text.sysConfig.menuTaxeGroup, width=15, command= lambda: groupTaxeInfo())
    taxeGroupButton.config(state=state2)
    
    storeInfoButton.grid(row=1, column=1, pady=(5,0))
    taxeButton.grid(row=2,column=1, pady=(5,0))
    taxeGroupButton.grid(row=3, column=1, pady=(5,0))
    languageButton.grid(row=4,column=1, pady=(5,0))    
    databaseButton.grid(row=5, column=1, pady=(5,0))    
    
    rightSubFrame.pack(fill="both", side="right", expand=True)
    leftSubFrame.pack(side="left", anchor="w", fill="y", expand=True)   
    bottomFrame.pack(side="bottom", fill="y", anchor="w", expand=True)
    
'''
function to open group taxe information
'''
def groupTaxeInfo():
        
    state = "disabled"
    
    groupTaxeField= tk.StringVar()
    
    if (connectedUser.level == 3):
        state = "normal"
    
    try:
        rightSubFrame.destroy()#try to destroy bottomFram if exist
    except:
        pass
    
    global rightSubFrame  
    rightSubFrame = tk.Frame(bottomFrame)#recreate a new bottom frame
    
    sql = """SELECT * FROM groupTaxe"""
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save user password
        
        groupTaxeData = cursor.fetchall()
                               
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
     
    groupTaxeTable = []
    
    if groupTaxeData == ():
        groupTaxeTable.append("")
    else:
    
        i = 0
    
        for groupTaxe in groupTaxeData:
            groupTaxeTable.append(groupTaxeData[i][1])
            i = i + 1
            
    groupTaxeMenu = tk.OptionMenu(rightSubFrame, groupTaxeField, *groupTaxeTable)
    groupTaxeMenu["menu"].config(bg="white")
    groupTaxeMenu.configure(width=26, bg="white")
    
    groupTaxeChoseButton = tk.Button(rightSubFrame, text=text.sysConfig.groupTaxeChooseButton, command= lambda: groupTaxeDetails(groupTaxeField.get()))
    groupTaxeNewButton = tk.Button(rightSubFrame, text=text.sysConfig.newGroupTaxeButton, command=lambda: newTaxe())
        
    groupTaxeMenu.grid(row=1, column=1, pady=(5,0))
    groupTaxeChoseButton.grid(row=1, column=2, pady=(5,0), padx=90)
    groupTaxeNewButton.grid(row=1, column=3, pady=(5,0), padx=(5,0), columnspan=2)
    
    rightSubFrame.pack(fill="x", pady=(5,0), expand=True, side="right", anchor="n")
    
'''
function to show details of group taxe
'''

def groupTaxeDetails(groupTaxe):
            
    if groupTaxe == "":
        tkm.showerror("", text.sysConfig.errorNoGroupTaxe)
        return
    
    sql = """SELECT * FROM groupTaxe WHERE groupName = '{0}'""".format(groupTaxe)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        groupTaxeData = cursor.fetchone()
                               
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()   
       
    groupNameData = tk.StringVar()
    groupCascadeData = tk.StringVar()
    groupMemberData = tk.StringVar()
    
    radioButtonFrame= tk.Frame(rightSubFrame, relief="ridge", borderwidth=3)
    memberButtonFrame = tk.Frame(rightSubFrame)
    groupButtonFrame = tk.Frame(rightSubFrame)
       
    groupNameLabel = tk.Label(rightSubFrame, text=text.sysConfig.groupNameLabel)
    groupNameField = tk.Entry(rightSubFrame, textvariable= groupNameData, bg="white", width=30)
    groupNameField.delete(0, "end")
    groupNameField.insert(0, groupTaxeData[1])
        
    groupCascadeLabel = tk.Label(radioButtonFrame, text=text.sysConfig.groupCascadeLabel)
    
    groupCascadeMenu = tk.OptionMenu(radioButtonFrame, groupCascadeData, text.sysConfig.cascadeYes, text.sysConfig.cascadeNo)
    
    if groupTaxeData[2] == 1:
        groupCascadeData.set(text.sysConfig.cascadeYes)
    else:
        groupCascadeData.set(text.sysConfig.cascadeNo)
        
    
    sql = "SELECT * FROM taxesGroupTaxe WHERE groupTaxeID = '{0}' ORDER BY priority".format(groupTaxeData[0])
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        memberList = cursor.fetchall()
                              
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
    i=1
    
    memberFrame = tk.Frame(rightSubFrame)
    tk.Label(memberFrame, text="Taxe").grid(row=0, column=1)
    tk.Label(memberFrame, text="Ordre").grid(row=0, column=2)        
    
    order = {}
    for member in memberList:
        sql2 = "SELECT * FROM Taxes WHERE ID = '{0}'".format(member[1])
        
        try:        
            connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
            cursor= connection.cursor()
        
            cursor.execute(sql2)#request to get taxe information
        
            memberTaxe = cursor.fetchone()
                               
        except mdb.Error, e:
            print "Error: {0} {1}".format(e.args[0], e.args[1])
            sys.exit(1)
            
        finally:
            if connection:
                connection.close()
        #groupMemberListBox.insert("end", memberTaxe[1]+":"+memberTaxe[2])
        
               
        tk.Label(memberFrame, text=memberTaxe[1] + ":" + memberTaxe[2]).grid(row=i, column=1, pady=(5,0))
        e = tk.Entry(memberFrame, bg="white", width=5)
        e.insert(0, member[3])
        e.grid(row=i, column=2, pady=(5,0))
        order[memberTaxe[1]] = e
        i = i+1
        
        
    addMemberButton = tk.Button(memberButtonFrame, width=10, text=text.sysConfig.addMemberButton, command=lambda: addTaxeToGroup(groupTaxeData[0]))
    
    removeMemberButton = tk.Button(memberButtonFrame, width=10, text=text.sysConfig.removeMemberButton)
         
    groupNameLabel.grid(row=2, column=1, pady=(5,0))
    groupNameField.grid(row=2, column=2, pady=(5,0))
    
    radioButtonFrame.grid(row=2, column=3, pady=(5,0))
    
    groupCascadeLabel.grid(row=1, column=1, pady=(5,0))
    groupCascadeMenu.grid(row=2, column=1, pady=(5,0))
    
    addMemberButton.grid(row=1, column=1, pady=(5,0))
    
    removeMemberButton.grid(row=4, column=1, pady=(5,0))
    
    saveGroupButton = tk.Button(groupButtonFrame, text=text.sysConfig.saveGroup)
    deleteGroupButton = tk.Button(groupButtonFrame, text=text.sysConfig.deleteGroup)
    
    saveGroupButton.grid(row=1, column=1, padx=(5,0))
    deleteGroupButton.grid(row=1, column=2, padx=(5,0))
    
    memberFrame.grid(row=3, column=2, pady=(5,0), columnspan=1)
    memberButtonFrame.grid(row=3, column=1)
    groupButtonFrame.grid(row=4, column=1, columnspan=3, pady=(5,0))
    
   
'''
function to add taxe to group
''' 
def addTaxeToGroup(groupID):
    
    global addTaxeWindow
    addTaxeWindow = tk.Toplevel(window)
    addTaxeWindow.title(text.sysConfig.addTaxeWindow)
    addTaxeWindow.geometry("400x75+0+0")
    
    availabeTaxe = []
    selectedTaxe = tk.StringVar()
    
    sql = "SELECT * FROM Taxes"
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        allTaxes = cursor.fetchall()
                              
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    sql = "SELECT TaxesID FROM taxesGroupTaxe WHERE groupTaxeID = '{0}'". format(groupID)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        usedTaxes = cursor.fetchall()
                              
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()    
    
    nonAvailable = []
    for taxe in usedTaxes:
        nonAvailable.append(taxe[0])    
             
    for taxe in allTaxes:         
        if not taxe[0] in nonAvailable:
           availabeTaxe.append(taxe)
           
    if availabeTaxe == []:
        taxeMenu = tk.OptionMenu(addTaxeWindow, selectedTaxe, *" ")
    else:
        taxeMenu = tk.OptionMenu(addTaxeWindow, selectedTaxe, *availabeTaxe)
    
    taxeMenLabel = tk.Label(addTaxeWindow, text=text.sysConfig.chooseTaxe)
    addButton = tk.Button(addTaxeWindow, text=text.sysConfig.addMemberButton, command=lambda: saveAdditionGroup(groupID, selectedTaxe.get()))
    cancelButton = tk.Button(addTaxeWindow, text=text.sysConfig.cancelButton, command=lambda: addTaxeWindow.destroy())
    
    taxeMenLabel.grid(row=1, column=1)
    taxeMenu.grid(row=1, column=2)
    addButton.grid(row=2, column=1)
    cancelButton.grid(row=2, column=2)
    
'''
function to save the new taxe in the group
'''
    
def saveAdditionGroup(groupID, taxeID):
    
    if taxeID == "":
        tkm.showerror("", text.sysConfig.noTaxe)
        return
    
    sql = "SELECT MAX(priority) FROM taxesGroupTaxe WHERE groupTaxeID = '{0}'".format(groupID)
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        maxPriority = cursor.fetchone()
                              
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
    max= maxPriority[0]
    sql = "INSERT INTO taxesGroupTaxe(taxesID, groupTaxeID, priority) VALUES('{0}', '{1}', '{2}')".format(taxeID[2], groupID, max+1)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save taxe info
            
        connection.commit()#commit change
          
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
    
    sql = "SELECT * FROM groupTaxe WHERE ID = '{0}'".format(groupID)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        groupeData = cursor.fetchone()
                              
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
                  
    tkm.showinfo("", text.sysConfig.taxeAdded)
    groupTaxeDetails(groupeData[1])
    addTaxeWindow.destroy()
    
    
'''
function to open taxe information
'''
def taxeInfo():
    
    global taxeNameData
    global taxeDescriptionData
    global taxeRateData
    
    taxeNameData = tk.StringVar()
    taxeDescriptionData = tk.StringVar()
    taxeRateData= tk.StringVar()
    
    state = "disabled"
    
    taxeField= tk.StringVar()
    
    if (connectedUser.level == 3):
        state = "normal"
    
    try:
        rightSubFrame.destroy()#try to destroy bottomFram if exist
    except:
        pass
    
    global rightSubFrame  
    rightSubFrame = tk.Frame(bottomFrame)#recreate a new bottom frame
    
    sql = """SELECT * FROM Taxes"""
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save user password
        
        taxeData = cursor.fetchall()
                               
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
    
    taxeTable = []
    
    i = 0
    
    for taxe in taxeData:
        taxeTable.append(taxeData[i][1])
        i = i + 1
            
    taxeMenu = tk.OptionMenu(rightSubFrame, taxeField, *taxeTable)
    taxeMenu["menu"].config(bg="white")
    taxeMenu.configure(width=26, bg="white")
    
    taxeChoseButton = tk.Button(rightSubFrame, text=text.sysConfig.taxeChoseButton, command= lambda: taxeDetails(taxeField.get()))
    taxeNewButton = tk.Button(rightSubFrame, text=text.sysConfig.taxeNewButton, command=lambda: newTaxe())
        
    taxeMenu.grid(row=1, column=1, pady=(5,0))
    taxeChoseButton.grid(row=1, column=2, pady=(5,0), padx=(31,31))
    taxeNewButton.grid(row=1, column=3, pady=(5,0), padx=(5,0))
    
    rightSubFrame.pack(fill="x", pady=(5,0), expand=True, side="right", anchor="n")
    
'''
function to add a new tax to the system
'''

def newTaxe():
    
    global newTaxeWindow
    
    taxeNameData = tk.StringVar()
    taxeDescriptionData = tk.StringVar()
    taxeRateData= tk.StringVar()
    
    newTaxeWindow = tk.Toplevel(window)
    newTaxeWindow.title(text.sysConfig.newTaxeWindowTitle)
    
    taxeNameLabel = tk.Label(newTaxeWindow, text=text.sysConfig.taxeNameLabel)
    taxeNameField = tk.Entry(newTaxeWindow, textvariable= taxeNameData, bg="white", width=30)
    taxeNameField.focus()
    
    taxeDescriptionLabel = tk.Label(newTaxeWindow, text=text.sysConfig.taxeDescription)
    taxeDescriptionField = tk.Entry(newTaxeWindow, textvariable= taxeDescriptionData, bg="white", width=30)
    
    taxeRateLabel = tk.Label(newTaxeWindow, text=text.sysConfig.taxeRates)
    taxeRateField = tk.Entry(newTaxeWindow, textvariable=taxeRateData, bg="white", width=30)
    
    taxeSaveButton = tk.Button(newTaxeWindow, text=text.sysConfig.saveNewTaxe, command=lambda :saveNewTaxe(taxeNameData.get(), taxeDescriptionData.get(), taxeRateData.get()))
    taxeCancelButton = tk.Button(newTaxeWindow, text=text.sysConfig.cancelNewTaxe, command= lambda: newTaxeWindow.destroy())
    
    taxeNameLabel.grid(row=1, column=1, pady=(5,0))
    taxeNameField.grid(row=1, column=2, pady=(5,0), padx=(0,25))
    
    taxeDescriptionLabel.grid(row=2, column=1, pady=(5,0))
    taxeDescriptionField.grid(row=2, column=2, pady=(5,0), padx=(0,25))
    
    taxeRateLabel.grid(row=3, column=1, pady=(5,0))
    taxeRateField.grid(row=3, column=2, pady=(5,0), padx=(0,25))
    
    taxeSaveButton.grid(row=4, column=1, pady=(5,0), padx=(25,0))
    taxeCancelButton.grid(row=4, column=2, pady=(5,0))
    
'''
function to save new taxe
'''
def saveNewTaxe(name, description, rate):
    sql = """INSERT INTO Taxes(Taxe, Description, Rate) VALUES('{0}', '{1}', '{2}')""".format(name, description, rate)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save taxe info
            
        connection.commit()#commit change
          
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    tkm.showinfo("", text.sysConfig.newTaxeSaved)
    
    newTaxeWindow.destroy()
    taxeInfo()
    
'''
function to show taxe details
'''

def taxeDetails(taxe):
            
    if taxe == "":
        tkm.showerror("", text.sysConfig.errorNoTaxe)
        return
    
    sql = """SELECT * FROM Taxes WHERE Taxe = '{0}'""".format(taxe)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to get taxe information
        
        taxeData = cursor.fetchone()
                               
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
           
    taxeNameLabel = tk.Label(rightSubFrame, text=text.sysConfig.taxeNameLabel)
    taxeNameField = tk.Entry(rightSubFrame, textvariable=taxeNameData, bg="white", width=30)
    taxeNameField.delete(0, "end")
    taxeNameField.insert(0, taxeData[1])
    
    taxeDescriptionLabel = tk.Label(rightSubFrame, text=text.sysConfig.taxeDescription)
    taxeDescriptionField = tk.Entry(rightSubFrame, textvariable=taxeDescriptionData, bg="white", width=30)
    taxeDescriptionField.delete(0, "end")
    taxeDescriptionField.insert(0, taxeData[2])
    
    taxeRateLabel = tk.Label(rightSubFrame, text=text.sysConfig.taxeRates)
    taxeRateField = tk.Entry(rightSubFrame, textvariable = taxeRateData, bg="white", width=30)
    taxeRateField.delete(0, "end")
    taxeRateField.insert(0, taxeData[3])
    
    taxeEditButton = tk.Button(rightSubFrame, text=text.sysConfig.taxeEditButton, command= lambda: saveTaxeChange(taxeData[0], taxeNameData.get(), taxeDescriptionData.get(), taxeRateData.get()))
    taxeDeleteButton = tk.Button(rightSubFrame, text=text.sysConfig.taxeDeleteButton, command= lambda: deleteTaxe(taxeData))
        
    taxeNameLabel.grid(row=2, column=1, pady=(5,0))
    taxeNameField.grid(row=2, column=2, pady=(5,0), columnspan=2)
    
    
    taxeDescriptionLabel.grid(row=3, column=1, pady=(5,0))
    taxeDescriptionField.grid(row=3, column=2, pady=(5,0), columnspan=2)
    
    taxeRateLabel.grid(row=4, column=1, pady=(5,0))
    taxeRateField.grid(row=4, column=2, pady=(5,0), columnspan=2)
    
    taxeEditButton.grid(row=5, column=1, pady=(5,0), columnspan=2)
    taxeDeleteButton.grid(row=5, column=2, pady=(5,0), columnspan=2)
    
'''
function to delete a taxe from the system
'''
def deleteTaxe(taxeData):
    confirm = tkm.askquestion(text.sysConfig.deleteTaxeConfirmTitle.format(taxeData[1]), text.sysConfig.deleteTaxeConfirm.format(taxeData[1] + " " + taxeData[2]))
    
    if confirm == "yes":
        sql = "DELETE FROM taxesGroupTaxe WHERE TaxesID = '{0}'".format(taxeData[0])#sql to delete all relation between the taxe and a taxeGroup
        
        try:        
            connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
            cursor= connection.cursor()
        
            cursor.execute(sql)#request to save taxe info
            
            connection.commit()#commit change
          
        except mdb.Error, e:
            print "Error: {0} {1}".format(e.args[0], e.args[1])
            sys.exit(1)
            
        finally:
            if connection:
                connection.close()
                
        sql = "DELETE FROM Taxes WHERE ID = '{0}'".format(taxeData[0])
        
        try:        
            connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
            cursor= connection.cursor()
        
            cursor.execute(sql)#request to save taxe info
            
            connection.commit()#commit change
          
        except mdb.Error, e:
            print "Error: {0} {1}".format(e.args[0], e.args[1])
            sys.exit(1)
            
        finally:
            if connection:
                connection.close()
        tkm.showinfo(text.sysConfig.taxeDeletedTitle, text.sysConfig.taxeDeleted)         
        taxeInfo()
    else:
        return
        
'''
function to save the modification made on taxe
'''
def saveTaxeChange(ID, taxe, taxeDescription, taxeRate):
    sql = "UPDATE Taxes SET Taxe = '{0}', Description = '{1}', Rate = '{2}' WHERE ID = {3}".format(taxe, taxeDescription, taxeRate, ID)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save taxe info
            
        connection.commit()#commit change
          
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    tkm.showinfo("", text.sysConfig.taxeChanged)
    
'''
function to open the buisness information configuration
'''
def storeInfo():
    state = "disabled"
    
    storeNameData = tk.StringVar()
    storeEmailData= tk.StringVar()
    storeAddressData = tk.StringVar()
    storePhoneData = tk.StringVar()
    storeCityData = tk.StringVar()
    storeProvinceData = tk.StringVar()
    storePostalCodeData = tk.StringVar()
    
    if (connectedUser.level == 3):
        state = "normal"
    
    try:
        rightSubFrame.destroy()#try to destroy bottomFram if exist
    except:
        pass
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute("""SELECT * FROM storeData""")#request to save user password
        
        storeData = cursor.fetchone()
                       
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
            
    global rightSubFrame  
    rightSubFrame = tk.Frame(bottomFrame)#recreate a new bottom frame
    
    storeInfoLabel = tk.Label(rightSubFrame, text=text.sysConfig.storeInfoTitleLabel, font=(16))
    
    storeNameLabel = tk.Label(rightSubFrame, text=text.sysConfig.storeNameLabel)
    storeNameField = tk.Entry(rightSubFrame, textvariable=storeNameData, bg="white", width=30)
    storeNameField.insert(0, storeData[1])
    
    storeEmailLabel = tk.Label(rightSubFrame, text=text.sysConfig.storeEmailLabel)
    storeEmailField = tk.Entry(rightSubFrame, textvariable=storeEmailData, bg="white", width=30)
    storeEmailField.insert(0, storeData[7])
    
    storeAddressLabel = tk.Label(rightSubFrame, text=text.sysConfig.storeAddressLabel)
    storeAddressField = tk.Entry(rightSubFrame, textvariable=storeAddressData, bg="white", width=30)
    storeAddressField.insert(0, storeData[2])
    
    storePhoneLabel = tk.Label(rightSubFrame, text=text.sysConfig.storePhoneLabel)
    storePhoneField = tk.Entry(rightSubFrame, textvariable=storePhoneData, bg="white", width=10)
    storePhoneField.insert(0, storeData[6])
    
    storeCityLabel = tk.Label(rightSubFrame, text=text.sysConfig.storeCityLabel)
    storeCityField = tk.Entry(rightSubFrame, textvariable=storeCityData, bg="white", width=20)
    storeCityField.insert(0, storeData[4])
    storeProvinceLabel = tk.Label(rightSubFrame, text=text.sysConfig.storeProvinceLabel)
    storeProvinceField = tk.Entry(rightSubFrame, textvariable=storeProvinceData, bg="white", width=20)
    storeProvinceField.insert(0, storeData[5])
    storePostalCodeLabel = tk.Label(rightSubFrame, text=text.sysConfig.storePostalCodeLabel)
    storePostalCodeField = tk.Entry(rightSubFrame, textvariable=storePostalCodeData, bg="white", width=10)
    storePostalCodeField.insert(0, storeData[3])
    
    storeSaveButton = tk.Button(rightSubFrame, text=text.sysConfig.storeSaveButton, command= lambda: saveStoreInfo(storeNameData.get().encode("utf-8"), storeAddressData.get().encode("utf-8"), storePostalCodeData.get().encode("utf-8"), storeCityData.get().encode("utf-8"), storeProvinceData.get().encode("utf-8"), storePhoneData.get().encode("utf-8"), storeEmailData.get().encode("utf-8")))
    storeSaveButton.config(state=state)
    
    storeInfoLabel.grid(row=1, column=1, columnspan=6, pady=(5,0))
    storeNameLabel.grid(row=2, column=1, pady=(5,0), columnspan=1)
    storeNameField.grid(row=2,column=2, pady=(5,0), columnspan=2)
    storeEmailLabel.grid(row=2, column=4, pady=(5,0), padx=(10,0), columnspan=1)
    storeEmailField.grid(row=2, column=5, pady=(5,0), columnspan=2)
    storeAddressLabel.grid(row=3, column=1, pady=(5,0), columnspan=1)
    storeAddressField.grid(row=3, column=2, pady=(5,0), columnspan=2)
    storePhoneLabel.grid(row=3, column=4, pady=(5,0), padx=(10,0), columnspan=1)
    storePhoneField.grid(row=3, column=5, pady=(5,0), columnspan=2)
    storeCityLabel.grid(row=4, column=1, pady=(5,0))
    storeCityField.grid(row=4, column=2, pady=(5,0))
    storeProvinceLabel.grid(row=4, column=3, pady=(5,0), padx=(10,0))
    storeProvinceField.grid(row=4, column=4, pady=(5,0))
    storePostalCodeLabel.grid(row=4, column=5, pady=(5,0), padx=(10,0))
    storePostalCodeField.grid(row=4, column=6, pady=(5,0))
    storeSaveButton.grid(row=5, column=1, columnspan=6, pady=(5,0))
    
    rightSubFrame.pack(fill="x", pady=(5,0), expand=True, side="right", anchor="n")
    
'''
function to save storeInfo
'''
def saveStoreInfo(storeName, storeAddress, storePostalCode, storeCity, storeProvince, storePhone, storeEmail):
    
    sql = """UPDATE storeData SET storeName = '{0}', storeAddress = '{1}', storePostalCode = '{2}', storeCity = '{3}', storeProvince = '{4}', storePhone = '{5}', storeEmail = '{6}' WHERE ID = 1""".format(storeName, storeAddress, storePostalCode, storeCity, storeProvince, storePhone, storeEmail)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save shop info
            
        connection.commit()#commit shop Info
          
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
    
    tkm.showinfo("", text.sysConfig.storeDataSaved)
    sysConfig()

'''
function to show the language configuration
'''        
def langConfig():
    
    availableLanguages = getLanguages()#get table of all available language pack in folder
    languageField = tk.StringVar()
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute("""SELECT language FROM sysConfig""")#request to save user password
            
        defaultLanguage = cursor.fetchone()[0]
           
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
                    
    finally:
        if connection:
            connection.close()  
    
    try:
        rightSubFrame.destroy()#try to destroy bottomFram if exist
    except:
        pass
    
    global rightSubFrame  
    rightSubFrame = tk.Frame(bottomFrame)#recreate a new bottom frame
    
    languageTitleLabel = tk.Label(rightSubFrame, text=text.sysConfig.languageTitleLabel, font=(16))
    languageLabel = tk.Label(rightSubFrame, text=text.sysConfig.languageLabel)
    languageSaveButton = tk.Button(rightSubFrame, text=text.sysConfig.languageSaveButton, command= lambda: saveLanguage(languageField.get()))  
    
    languageMenu = tk.OptionMenu(rightSubFrame, languageField, *availableLanguages)
    languageMenu["menu"].config(bg="white")
    languageMenu.configure(width=26, bg="white")
    languageField.set(defaultLanguage)
    
    
    languageTitleLabel.grid(row=1, column=1, columnspan=2)
    languageLabel.grid(row=2, column=1, pady=(5,0))
    languageMenu.grid(row=2, column=2, pady=(5,0))    
    languageSaveButton.grid(row=3, column=1, pady=(5,0), columnspan=2)
    
    rightSubFrame.pack(fill="x", pady=(5,0), expand=True, side="right", anchor="n")
    
'''
function to save language configuration
'''
def saveLanguage(language):
    
    #import the next language pack to display nex reboot message
    langFile = "Languages.language_" + language
    __import__(langFile)
    nextLang = sys.modules[langFile]
    
    sql = """UPDATE sysConfig SET language = '{0}' WHERE id = 1""".format(language)
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute(sql)#request to save language selection
            
        connection.commit()#commit language
           
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()
    tkm.showinfo("", nextLang.sysConfig.nextRebootText)
    
'''
function to get all the language files available in the languages folder
'''
def getLanguages():

    languagesFolder = "./Languages"
    
    languageFiles = []#create empty table to store availabe language availabel in folder
    
    for file in os.listdir(languagesFolder):
        if (file[:-8] == "language"):#if it's a language file
            language = file[-7:]#remvove the language_ frome the filename
            language = language[:-3]#remove .py frome the filename
            languageFiles.append(language)#andd language to table
    return languageFiles 
    

##################################### - START THE PROGRAM - #####################################
startProgram()