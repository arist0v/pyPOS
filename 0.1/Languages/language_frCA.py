# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v
Language Pack for French Canada
include all text from the Program
'''
'''
class for text on the main text, program name, version, author etc...
'''

class mainSoftwareText:
    
    def __init__(self):
        self.program = "pyPOS"
        self.mainWindowTitle = "pyPOS - Point de vente, Système de facturation en Python"
        self.author = "Martin Verret"
        self.contact = "https://github.com/arist0v/pyPOS"

mainText = mainSoftwareText()
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
        self.config = "Configuration"# configuration menu button
        self.userLogged= "Utilisateur : "
        self.locale = "fr_CA.utf8"#set the locale for the clock and date
        
menu = menuScreen()

'''
text for the user manager screen
'''

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
        self.deleteUserButton = "Supprimer"
                
userManager = userManagerScreen()

'''
text for the delete user popup
'''

class deleteUserScreen:
    
    def __init__(self):
        self.windowTitle = "Supression"
        self.deleteConfrim = "Voulez vous vraiment supprimer l'utilisateur : "
        self.confirm = "Utilisateur "
        self.confirm2 = " supprimé"
        
deleteUser = deleteUserScreen()

'''
text for the change password screen
'''

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

'''
text fort the new user screen
'''

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
        self.wrongConfirm = "Les mots de passe ne sont pas identiques"
        self.errorTitle = "Erreur"
        self.noFirstName = "Vous devez inscrire un prénom"
        self.noLastName = "Vous devez inscrire un nom de famille"
        self.noUsername = "Vous devez inscrire un nom d'utilisateur"
        self.userAddedTitle = "Ajout d'utilisateur"
        self.userAdded = "Utilisateur ajouté"
                
newUser = newUserScreen()

'''
text for the systeme configuration screen
'''

class sysConfigScreen:
    
    def __init__(self):
        self.menuLanguage = "Langue"#menu button for language config
        self.menuDatabase = "Base de données"#database configuration menu buttun
        self.menuTaxe = "Taxe"#tax configuration menu button
        self.menuTaxeGroup = "Groupe de taxes"#taxes group configuration menu button
        self.menuStoreInfo = "Info Boutique"#shop info configurations
        self.languageTitleLabel = "Configuration de la langue"#title of language config
        self.languageLabel = "Langue :"
        self.languageSaveButton = "Sauvegarder"
        self.nextRebootText = "Les modifications seront apportées au prochain démarrage de l'application."
        self.storeInfoTitleLabel = "Information sur la boutique"
        self.storeNameLabel = "Nom de la boutique :"#store name
        self.storeEmailLabel = "Courriel :"#email adresse of the store
        self.storeAddressLabel = "Adresse :"
        self.storePhoneLabel = "Téléphone :"
        self.storeCityLabel = "Ville :"
        self.storeProvinceLabel = "Province :"
        self.storePostalCodeLabel = "Code Postal :"
        self.storeSaveButton = "Sauvegarder"
        self.storeDataSaved = "Information sauvegardé"
        self.taxeChoseButton = "Choisir"
        self.errorNoTaxe = "Vous devez choisir une taxe!"
        self.taxeNameLabel = "Taxe :"
        self.taxeDescription = "Numéro :"
        self.taxeRates = "Taux(%) :"
        self.taxeEditButton = "Modifier"
        self.taxeChanged = "Modification apporté"
        self.taxeNewButton = "Nouvelle taxe"
        self.taxeDeleteButton = "Supprimer"
        self.newTaxeWindowTitle = "Ajout d'une nouvelle taxe"
        self.saveNewTaxe = "Sauvegarder"
        self.cancelNewTaxe = "Annuler"
        self.newTaxeSaved = "Nouvelle taxe ajouté!"
        self.newGroupTaxeButton = "Nouveau Groupe de taxes"
        self.groupTaxeChooseButton = "Choisir"
        self.errorNoGroupTaxe = "Vous devez choisir un groupe"
        self.groupNameLabel = "Nom du groupe :"
        self.groupCascadeLabel = "Cascade"
        self.cascadeYes = "Oui"
        self.cascadeNo = "Non"
        self.addMemberButton = "Ajouter"
        self.saveMemberButton = "Sauvgarder"
        self.removeMemberButton = "Supprimer"
        self.addTaxeWindow = "Ajouter une taxe au groupe"
        self.saveGroup = "Sauvegarder"
        self.deleteGroup = "Supprimer"
        self.chooseTaxe = "Choisissez une taxe :"
        self.cancelButton= "Annuler"
        self.noTaxe = "Vous devez choisir une taxe"
        self.taxeAdded = "Taxe ajouté au groupe"
        self.deleteTaxeConfirmTitle = "Suppresion de la taxe :"
        self.deleteTaxeConfirm = "Voulez vous vraiement supprimer la taxe {0}?"
        self.taxeDeletedTitle = "Supprimé"
        self.taxeDeleted = "La taxe à été supprimé"
        self.orderSaved = "L'ordre a été modifié"
        self.removeTaxeWindow = "Supprimer une taxe du groupe {0}"
        self.removeTaxeButton = "Supprimer"
        self.confirmRemove = "Voulez vous vraiment retiré la taxe : {0}, du groupe: {1}"
        self.taxeRemoved = "La taxe a été retiré du groupe."
        self.groupSaved = "Les informations ont été sauvegardé"
        self.groupNotEmpty  = "Le groupe doit être vide pour pouvoir être supprimé"
        self.groupDeleted = "Le groupe a été supprimé"
        self.confirmDelete = "Êtes vous sûre de vouloir supprimer ce groupe"
        self.newGroupWindowTitle = "Ajout d'un groupe de taxes"
        self.groupNameLabel = "Nom du groupe :"
        self.noGroupName = "Vous devez inscrire un nom pour le groupe"
        self.newGroupSaved = "Le nouveau groupe a été créer"
        self.backupButton = "Sauvegarder"
        self.restoreButton = "Restaurer"
        self.backupDone = "Sauvegarde Effectué"
        self.backupError = "Erreur lors de la sauvegarde"
        self.restoreDone = "La base de données a été restauré"
        self.restoreError = "Erreur lors de la restauration"
        
sysConfig = sysConfigScreen()