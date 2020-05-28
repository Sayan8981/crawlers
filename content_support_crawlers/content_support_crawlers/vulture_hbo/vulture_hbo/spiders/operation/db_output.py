import MySQLdb
import sys
import os
import db_detail
import datetime
import csv
from datetime import datetime,timedelta

class db_output_stats:

    def __init__(self):  
        self.db_list=[]
        self.connection=''
        self.cursor=''
        self.fieldnames=["title","year","content_available","Show_type","content_defination","updated_db"]

    def set_up_db_connection(self):
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user="%s"%db_detail.username,passwd="%s"%db_detail.passwd,db=db_detail.database_name)
        self.cursor=self.connection.cursor()     

    #TODO: creating file for writing
    def create_csv(self,result_sheet):
        if (os.path.isfile(os.getcwd()+result_sheet)):
            os.remove(os.getcwd()+result_sheet)
        csv.register_dialect('csv',lineterminator = '\n',skipinitialspace=True,escapechar='')
        output_file=open(os.getcwd()+result_sheet,"w")
        return output_file

    def main(self):
        self.set_up_db_connection()
        result_sheet='/operation/attachments/hbo_added_content_%s.csv'%(datetime.now().strftime('%b %d, %Y'))
        output_file=self.create_csv(result_sheet)
        with output_file as outputcsvfile:
            self.writer= csv.writer(outputcsvfile,dialect="csv",lineterminator = '\n')
            self.writer.writerow(self.fieldnames)
            query="select title,year, content_available,content_category,content_defination,updated_db from {table_name}".format(table_name=db_detail.table)
            self.cursor.execute(query)
            result=self.cursor.fetchall()
            self.writer.writerows(result)

        output_file.close()
        self.connection.close()    

  



