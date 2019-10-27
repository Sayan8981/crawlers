import os
import sys
import scrapy
import mysql.connector


class create_db_tables:
    def __init__(self):
        self.database="TOI_news"
        self.username='root'
        self.password='root@123'
        self.db_list=[]
        self.connection=''
        self.cursor=''

    def set_up_db_connection(self):
        #import pdb;pdb.set_trace()
        self.connection=mysql.connector.connect(host="localhost",user="%s"%self.username,passwd="%s"%self.password)
        self.cursor=self.connection.cursor()    

    def create_require_db_tables(self):
        #import pdb;pdb.set_trace()
        self.set_up_db_connection()
        self.cursor.execute("show databases;")
        for db in self.cursor:
            self.db_list.append(db[0].encode())
        #import pdb;pdb.set_trace() 
        if self.database not in self.db_list:
            self.cursor.execute("create database %s;"%self.database)
            print("\n %s db created"%self.database) 
            self.cursor.execute("use %s;"%self.database)
            create_tables=["create table TOI_news_details (sk_key varchar(500) primary key, News_headlines varchar(1000), News_details varchar(50000), State varchar(100),City varchar(100),Dump_updated varchar(100),News_Updated varchar(200), News_url varchar(1000));"]
            for query in create_tables: 
                self.cursor.execute(query)  
            print("\n")    
            print("Table created.................")             
        else:
            print("%s db is already exist"%self.database)
            self.cursor.execute("use %s;"%self.database)
            self.cursor.execute("show tables;")
            table_cursor=self.cursor.fetchall()
            if not table_cursor:
                create_tables=["create table TOI_news_details (sk_key varchar(500) primary key, News_headlines varchar(1000), News_details varchar(50000), State varchar(100),City varchar(100),Dump_updated varchar(100),News_Updated varchar(200), News_url varchar(1000));"]
                for query in create_tables:
                    self.cursor.execute(query) 
                print ("table created.......")    
            else:
                print ("\n")
                print("Table is already exist in DB",table_cursor)
        self.connection.close()        
                               

object_=create_db_tables()
object_.create_require_db_tables()