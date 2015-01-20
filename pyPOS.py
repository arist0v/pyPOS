# -*- coding: latin1 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v

Point of Sale system for managed retail store
Main file of the system

'''
import dbConfig#import database configuration file

import _mysql#import mysql connector library
import sys#import system database

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
function to import the language file
'''
def importLanguage(language):
    
    if (language == "frCA"):#if language is French Canadian
        import language_frCA as text#import the language file
        
    else:
        print "Wrong Language"
        sys.exit(1)

importLanguage(language())#import the correct language file library

