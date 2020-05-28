import MySQLdb
import sys
import os
import db_detail
import datetime
import csv
from datetime import datetime,timedelta

#TODO: To print CSV file from DB 
class db_output_stats:

    def __init__(self):  
        self.db_list=[]
        self.connection=''
        self.cursor=''
        self.fieldnames=["Netflix_Id","Title","Show_type","Description","Year","Rating","Duration","season_number","Audio","Url","Available_Seasons","Image","Genres","Director","Actor","Subtitles","Added_to_site","Content_type","Content_history","Updated_at"]

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
        result_sheet='/operation/attachments/USA_new_on_Netflix_%s.csv'%(datetime.now().strftime('%b %d, %Y'))
        output_file=self.create_csv(result_sheet)
        with output_file as outputcsvfile:
            self.writer= csv.writer(outputcsvfile,dialect="csv",lineterminator = '\n')
            self.writer.writerow(self.fieldnames)
            query="select Netflix_id,title,show_type,description,year,rating,duration,season_number,audio,url,available_season,image,genres,Director,Actor,subtitles,added_to_site,content_type,content_history,updated_at from {table_name} where updated_at='%s'".format(table_name=db_detail.table)
            self.cursor.execute(query%(datetime.now().strftime('%b %d, %Y')))
            result=self.cursor.fetchall()
            self.writer.writerows(result)

        output_file.close()
        self.connection.close()    

  



