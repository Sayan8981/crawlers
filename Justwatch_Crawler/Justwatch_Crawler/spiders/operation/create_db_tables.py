#import pdb;pdb.set_trace
import MySQLdb
import sys
import os
import db_detail


class createdbtable:

    def __init__(self):
        self.db_list=[]
        self.connection=''
        self.cursor=''
        self.create_tables=["CREATE TABLE %s (title varchar(254) NOT NULL,Show_type varchar(100) DEFAULT NULL,Source varchar(100) DEFAULT NULL,Service varchar(100) DEFAULT NULL,content_type varchar(100) DEFAULT NULL,Added_to_site varchar(200) DEFAULT NULL,Updated_at_DB varchar(200) DEFAULT NULL,year varchar(254) DEFAULT NULL,PRIMARY KEY (title)) ENGINE=InnoDB DEFAULT CHARSET=utf8"%db_detail.table]

    def set_up_db_connection(self):
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user="%s"%db_detail.username,passwd="%s"%db_detail.passwd)
        self.cursor=self.connection.cursor()   

    def create_require_db_tables(self):
        self.set_up_db_connection()
        self.cursor.execute("show databases;")
        for db in self.cursor:
            self.db_list.append(db[0])
        if db_detail.database_name not in self.db_list:
            self.cursor.execute("create database %s;"%db_detail.database_name) 
            self.cursor.execute("use %s;"%db_detail.database_name)
            for query in self.create_tables: 
                self.cursor.execute(query)  
            print("\n")    
            print("Table created.................")          
        else:
            print("%s db is already exist"%db_detail.database_name)
            self.cursor.execute("use %s;"%db_detail.database_name)
            self.cursor.execute("show tables;")
            table_cursor=self.cursor.fetchall()
            if not table_cursor:
                for query in self.create_tables:
                    self.cursor.execute(query) 
                print ("table created.......")    
            else:
                print ("\n")
                print("Table is already exist in DB",table_cursor)
        self.connection.close()                  

createdbtable().create_require_db_tables()