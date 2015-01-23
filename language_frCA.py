# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v
Language Pack for French Canada
include all text from the Program
'''

'''
class for text in the licence windows
'''

class licenceScreen:
    
    def __init__(self):
        self.title = "Licence GNU/GPL 3"
        
licence = licenceScreen()

'''
class for text in login screen
'''
class loginScreen:
    
    def __init__(self):
        
        self.quit = "Quitter"#Quit button
        self.login = "Connexion"#login button
        self.username = "Nom d'utilisateur :"#label for username textField
        self.password = "Mot de passe :"#label for password field
        self.message = "Veuillez vous identifier"
        self.invalidUser = "Nom d'utilisateur inconnu"
        self.invalidPass = "Mot de passe invalide"
        self.licence = "Ce logiciel est distribué sous licence GNU/GPL 3.0"
        
login = loginScreen()#generate the login screen text Variable

'''
class for text in the menu screen
'''
class menuScreen:
    
    def __init__(self):
        self.logout = "Déconnexion"#Logout Button
        self.user = "Utilisateur"#User menu button
        
menu = menuScreen()

class userManagerScreen:
    
    def __init__(self):
        self.userListLabel = "Liste des utilisateurs"#label over the userlist
        self.firstNameLabel = "Prénom :"
        self.lastNameLabel = "Nom :"
        self.emailLabel = "Courriel :"
        self.levelLabel = "Type :"
        self.levelUser = "Utilisateur"
        self.levelManager = "Gérant"
        self.levelAdmin = "Administrateur"
        self.changePassButton = "Modifiez le mot de passe"
        self.saveButton = "Sauvegarder"
        self.savePopUp = "Changement Sauvegardé"
        self.addUserButton = "Ajouter un Utilisateur"
        
userManager = userManagerScreen()

class changePasswordScreen:
    
    def __init__(self):
        self.windowTitle = "Modification du mot de passe"
        self.cancelButton = "Annuler"
        self.changeButton = "Modifier"
        self.instructionLabel = """Pour modifier le mot de passe, veuillez entrer votre ancien mot de passe, ou si vous modifiez le mot de passe d'un autre utilisateur, entrez votre propre mot de passe."""
        self.oldPass = "Mot de passe actuel :"
        self.newPass = "Mot de Passe :"
        self.confirmPass = "Confirmez le mot de passe :"
        self.badOldPass = "Ancien mot de passe invalide"
        self.badConfirm = "Les nouveaux mots de passe sont différent"
        self.onlyLower = "Le mot de passe doit contenir au moins une(1) majuscule"
        self.onlyUpper = "Le mot de passe doit contenir au moins une(1) minuscule"
        self.noDigit = "Le mot de passe doit contenir au moins un(1) chiffre"
        self.passShort = "Le mot de passe doit avoir au moins six(6) charactere"
        self.errorTitle = "Erreur"
        
changePassword = changePasswordScreen()

class newUserScreen:
    
    def __init__(self):
        self.firstNameLabel = "Prénom :"
        self.lastNameLabel = "Nom :"
        self.emailLabel = "Courriel :"
        self.levelLabel = "Type :"
        self.levelUser = "Utilisateur"
        self.levelManager = "Gérant"
        self.levelAdmin = "Administrateur"
        self.saveButton = "Sauvegarder"
        self.addedPopup = "Changement Sauvegardé"
        self.passwordLabel = "Mot de passe :"
        self.confirmPassLabel = "Confirmer le mot de passe :"
        self.usernameLabel = "Nom d'utilisateur :"
        
newUser = newUserScreen()
