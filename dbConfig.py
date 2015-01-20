# -*- coding: latin1 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v
DB configuration for the program
'''

'''
TODO:
import language dynamicly based on DB data for system language

'''
import _mysql#import mysql connector library

class server:
    '''
    class for the server connection to Mysql Database
    '''
    
    def __init__(self):
        
        self.server="localhost"#mysql server to connect
        self.user="pyPOS"#username for the server auth
        self.password="pyPOS"#password for the server auth
        self.database="POS"#database name

mysqlServer= server()
        



