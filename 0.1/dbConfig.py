# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2015-01-20

@author: arist0v
DB configuration for the program
'''

class server:
    '''
    class for the server connection to Mysql Database
    '''
    
    def __init__(self):
        
        self.server="localhost"#mysql server to connect
        self.user="POS"#username for the server auth
        self.password="POS"#password for the server auth
        self.database="POS"#database name
        self.port = "3306"
        
mysqlServer= server()
        



