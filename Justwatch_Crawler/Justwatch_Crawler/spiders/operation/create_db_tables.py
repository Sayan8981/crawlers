#import pdb;pdb.set_trace
import MySQLdb
import sys
import os
import db_detail
import logging

class createdbtable:

    def __init__(self):
        self.db_list=[]
        self.connection=''
        self.cursor=''
        self.create_movie_table_query = "CREATE TABLE %s (Movie_id int(200), Title varchar(254) DEFAULT NULL,Show_type varchar(100) DEFAULT NULL,Description TEXT DEFAULT NULL,Release_year int(200) DEFAULT NULL,original_title varchar(254) DEFAULT NULL,OTT TEXT DEFAULT NULL, Cast TEXT DEFAULT NULL,Duration varchar(200) DEFAULT NULL,Genres TEXT DEFAULT NULL,Rating TEXT DEFAULT NULL,Age_Rating varchar(100) DEFAULT NULL,Service_name varchar(100) DEFAULT NULL,Added_to_site varchar(100) DEFAULT NULL,Updated_at varchar(100) DEFAULT NULL,PRIMARY KEY (Movie_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8"%db_detail.movie_table

        self.create_series_table_query = "CREATE TABLE %s (Series_id int(200) DEFAULT NULL,Season_id int(200), Title varchar(254) DEFAULT NULL,Show_type varchar(100) DEFAULT NULL,Description TEXT DEFAULT NULL,Release_year int(200) DEFAULT NULL,original_title varchar(254) DEFAULT NULL, Cast TEXT DEFAULT NULL,Duration varchar(200) DEFAULT NULL,Season_number int(100),Genres TEXT DEFAULT NULL,Rating varchar(500) DEFAULT NULL,Age_Rating varchar(100) DEFAULT NULL,Service_name varchar(100) DEFAULT NULL,Added_to_site varchar(100) DEFAULT NULL,Updated_at varchar(100) DEFAULT NULL,PRIMARY KEY (Season_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8"%db_detail.Series_table

        self.create_episode_table_query = "CREATE TABLE %s (Series_id int(200) DEFAULT NULL,Season_id int(200) DEFAULT NULL,Episode_id int(200), Title varchar(254) DEFAULT NULL,Show_type varchar(100) DEFAULT NULL,Description TEXT DEFAULT NULL,OTT TEXT DEFAULT NULL, Duration varchar(200) DEFAULT NULL,season_number int(250) DEFAULT NULL,Episode_number int(250) DEFAULT NULL,Service_name varchar(100) DEFAULT NULL,Updated_at varchar(100) DEFAULT NULL,PRIMARY KEY (Episode_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8"%db_detail.Episodes_table

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
            self.create_table_query = [self.create_movie_table_query,self.create_series_table_query,self.create_episode_table_query]
            for query in self.create_table_query: 
                self.cursor.execute(query)  
            logging.info("\n")    
            logging.info("Tables created.................")          
        else:
            logging.info("%s db is already exist"%db_detail.database_name)
            self.cursor.execute("use %s;"%db_detail.database_name)
            self.cursor.execute("show tables;")
            table_cursor=self.cursor.fetchall()
            if (db_detail.movie_table,) not in table_cursor:
                self.cursor.execute(self.create_movie_table_query)
                logging.info ("%s table created......."%db_detail.movie_table)
            if (db_detail.Series_table,) not in table_cursor:
                self.cursor.execute(self.create_series_table_query)
                logging.info ("%s table created......."%db_detail.Series_table) 
            if (db_detail.Episodes_table,) not in table_cursor:
                self.cursor.execute(self.create_episode_table_query)
                logging.info ("%s table created......."%db_detail.Episodes_table)   
        self.connection.close()                  

createdbtable().create_require_db_tables()