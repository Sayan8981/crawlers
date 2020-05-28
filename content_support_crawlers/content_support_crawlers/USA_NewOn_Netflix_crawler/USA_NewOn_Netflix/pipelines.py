# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import os
import sys
import db_detail

class UsaNewonNetflixPipeline(object):
    def __init__(self):
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user='%s'%db_detail.username,passwd='%s'%db_detail.passwd,db='%s'%db_detail.database_name,charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 
        self.counter=0

    def process_item(self, item, spider):
        self.query="insert into {table_name} (Netflix_id,title,show_type,description,year,rating,duration,season_number,audio,url,available_season,image,genres,Director,Actor,subtitles,added_to_site,content_type,content_history,updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.table)
        self.cursor.execute(self.query,(item["netflix_id"],item["title"],item["show_type"],item["description"],item["year"],item["rating"],item["run_time"],item["season_number"],item["record_language"],item["url"],item["available_season"],item["image"],item["genres"],item["Director"],item["Actor"],item["subtitles"],item["added_to_site"],item["content_type"],item["history"],item["updated_at"]))
        self.counter+=1
        self.connection.autocommit(True)
        print("\n")
        print ("Total commit: ", self.counter)
        print("\n")
        return item
