import mysql.connector
import sys

class createdb_table:

    def __init__(self):
        self.database="Ceva_shipment"
        self.username=''
        self.password=''
        self.db_list=[]
        self.connection=''
        self.cursor=''

    def user_input(self):
        #import pdb;pdb.set_trace()
        self.username=sys.argv[1]
        self.password=sys.argv[2]    

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
            create_tables=["create table ceva_shipment_detail (waybill_number varchar(100) primary key, ship_date varchar(100), due_date varchar(200), estimated_delivery_date varchar(100), shipper_location varchar(100),consignee_location varchar(100),total_pcs varchar(200), actual_weight varchar(1000) ,charge_weight varchar(200), freight_terms varchar(100), service_level varchar(100), delivery_type varchar(100),movement_type varchar(100),history_data varchar(500));"]
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
                create_tables=["create table ceva_shipment_detail (waybill_number varchar(100) primary key, ship_date varchar(100), due_date varchar(200), estimated_delivery_date varchar(100), shipper_location varchar(100),consignee_location varchar(100),total_pcs varchar(200), actual_weight varchar(1000) ,charge_weight varchar(200), freight_terms varchar(100), service_level varchar(100), delivery_type varchar(100),movement_type varchar(100),history_data varchar(5000));"]
                for query in create_tables:
                    self.cursor.execute(query) 
                print ("table created.......")    
            else:
                print ("\n")
                print("Table is already exist in DB",table_cursor)
        self.connection.close()        
                           



createdb_table().create_require_db_tables()
        

        



    