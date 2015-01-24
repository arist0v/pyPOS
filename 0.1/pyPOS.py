# -*- coding: utf-8 -*-
#!/usr/bin/python
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
    import Languages.language_frCA as text#import the language file
else:
    print "Wrong Language"
    sys.exit(1)
      
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
    window.wm_title(text.mainText.mainWindowTitle + " " + text.mainText.version)#Title of windows
    #global h#global height
    #global w#blobal width
    h = window.winfo_screenheight()
    w = window.winfo_screenwidth()
    
    window.geometry("{0}x{1}+0+0".format(w, h))
    window.resizable(0, 0)


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
    
    global username#set a global username variable
    username = tk.StringVar()
    global password#set a global password variable
    password = tk.StringVar()
        
    messageLabel = tk.Label(mainFrame, text=text.login.message)
    usernameLabel = tk.Label(mainFrame, text=text.login.username)
    usernameField = tk.Entry(mainFrame, textvariable=username, width=30, bg="white")
    usernameField.bind('<Return>', lambda x: auth())#bind Return key when focus on username field
    usernameField.bind('<KP_Enter>', lambda x: auth())#numpad enter
    usernameField.focus()#set focuse on username first
    passwordLabel = tk.Label(mainFrame, text=text.login.password)
    passwordField = tk.Entry(mainFrame, textvariable=password, width=30, show="*", bg="white")
    passwordField.bind('<Return>', lambda x: auth())#bind Return key when focus on password field
    passwordField.bind('<KP_Enter>', lambda x: auth())#numpad enter
    
    loginButton = tk.Button(mainFrame, text=text.login.login, command= lambda: auth())#create login button
    loginButton.bind('<Return>', lambda x: auth())#bind Return key when focus on username field
    loginButton.bind('<KP_Enter>', lambda x: auth())#numpad enter
    quitButton = tk.Button(mainFrame, text=text.login.quit, command=window.quit)#create quit button
    licenceLabel = tk.Label(mainFrame, text=text.login.licence)
    licenceLabel.bind("<Button-1>",lambda x: showLicence())
    
    
    messageLabel.grid(row=1)   
    usernameLabel.grid(row=2)
    usernameField.grid(row=3)
    passwordLabel.grid(row=4)
    passwordField.grid(row=5)
    
    loginButton.grid(sticky="w", row=6, pady=5)
    quitButton.grid(sticky="e", row=6, pady=5)
    licenceLabel.grid(row=7)
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
    
    global bottomFrame
    bottomFrame = tk.Frame(mainFrame)#genereate the bottom frame
    
    userButton = tk.Button(upperFrame, text=text.menu.user, command= lambda: userManager(), borderwidth=1)
    configButton = tk.Button(upperFrame, text=text.menu.config, command=lambda: sysConfig())
    configButton.config(state=state)
    logoutButton = tk.Button(upperFrame, text=text.menu.logout, command=lambda : sysLogout(), borderwidth=1)
    

    userButton.grid(row=1, column=1)
    configButton.grid(row=1, column=2)
    logoutButton.grid(row=1, column=3)
    
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
    
    rightSubFrame.pack(fill="both", pady=25)
    
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
function to show the systeme configuration
'''        
def sysConfig():
    
    availableLanguages = getLanguages()#get table of all available language pack in folder
    languageField = tk.StringVar()
    
    try:        
        connection = mdb.connect(host=dbConfig.mysqlServer.server, user=dbConfig.mysqlServer.user, passwd=dbConfig.mysqlServer.password, db=dbConfig.mysqlServer.database)#connection to mysqldb
        
        cursor= connection.cursor()
        
        cursor.execute("""SELECT language FROM sysConfig""")#request to save user password
            
        defaultLanguage = cursor.fetchone()[0]
           
    except mdb.Error, e:
        print "Error: {0} {1}".format(e.args[0], e.args[1])
        sys.exit(1)
            
    finally:
        if connection:
            connection.close()  
    
    try:
        bottomFrame.destroy()#try to destroy bottomFram if exist
    except:
        pass
    
    global bottomFrame  
    bottomFrame = tk.Frame(mainFrame)#recreate a new bottom frame
    
    titleLabel = tk.Label(bottomFrame, text=text.sysConfig.titleLabel, font=(16))
    languageLabel = tk.Label(bottomFrame, text=text.sysConfig.languageLabel)  
    
    languageMenu = tk.OptionMenu(bottomFrame, languageField, *availableLanguages)
    languageMenu["menu"].config(bg="white")
    languageMenu.configure(width=26, bg="white")
    languageField.set(defaultLanguage)
    
    titleLabel.grid(row=1, column=1, columnspan=2)
    languageLabel.grid(row=2, column=1, pady=(5,0))
    languageMenu.grid(row=2, column=2, pady=(5,0))    
    
    bottomFrame.pack(side="bottom", fill="x", pady=(5,0))
    
'''
TODO:

Configuration du system
-langue
-devise
-taxe

'''
    
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