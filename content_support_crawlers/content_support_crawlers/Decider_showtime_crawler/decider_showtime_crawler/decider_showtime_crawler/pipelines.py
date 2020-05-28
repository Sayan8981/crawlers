# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import os
import sys
import db_detail


class DeciderCrawlerPipeline(object):
   def __init__(self):
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user='%s'%db_detail.username,passwd='%s'%db_detail.passwd,db='%s'%db_detail.database_name,charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 
        self.counter=0

   def process_item(self, item, spider):
        self.query="INSERT INTO {table_name} (title,category,ET_PT_timing,released,content_defination,updated_db,Service) VALUES (%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.table)
        self.cursor.execute(self.query,(item["title"],item["content_category"],item["ET_PT_timing"],item["content_released"],item["content_defination"],item["updated_db"],item["service"]))
        self.counter+=1
        self.connection.autocommit(True)
        print("\n")
        print ("Total commit: ", self.counter)
        print("\n")
        return item
