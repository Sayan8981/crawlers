import mysql.connector


class createdb_table:

    def __int__(self):
        self.database="Hindunews"
        self.username=''
        self.password=''
        self.db_list=[]
        self.connection=''
        self.cursor=''

    def user_input(self):
        print("Please enter your database_username")
        self.username=input(str)
        print("Please enter your database_password")
        self.password=input(str)    

    def set_up_db_connection(self):
        #import pdb;pdb.set_trace()
        self.connection=mysql.connector.connect(host="localhost",user="%s"%self.username,passwd="%s"%self.password)
        self.cursor=self.connection.cursor()    

    def create_require_db_tables(self):
        self.user_input()
        self.set_up_db_connection()
        self.cursor.execute("show databases;")
        for db in self.cursor:
            self.db_list.append(db[0].encode())
        #import pdb;pdb.set_trace() 
        if self.database not in self.db_list:
            self.cursor.execute("create database %s;"%self.database)
            print("\n %s db created"%self.database) 
            self.cursor.execute("use %s;"%self.database)
            create_tables=["create table National_news_details (sk_key varchar(500) primary key, News_headlines varchar(1000), News_intro varchar(2000), News_details varchar(50000), Country varchar(100),Date varchar(100),Updated_at varchar(200), News_url varchar(1000));"]
            for query in create_tables:
                self.cursor.execute(query)           
        else:
            print("%s db is already exist"%self.database)
            self.cursor.execute("use %s;"%self.database)
            self.cursor.execute("show tables;")
            table_cursor=self.cursor.fetchall()
            if not table_cursor:
                create_tables=["create table National_news_details (sk_key varchar(500) primary key, News_headlines varchar(1000), News_intro varchar(2000), News_details varchar(50000), Country varchar(100),Date varchar(100),Updated_at varchar(200), News_url varchar(1000));"]
                for query in create_tables:
                    self.cursor.execute(query) 
            else:
                print("Table is already exist in DB")
                           


object_=createdb_table()
object_.__int__()
object_.create_require_db_tables()
        

        



    