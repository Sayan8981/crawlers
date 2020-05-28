# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import os
import sys
import db_detail

class RecentlyAddedContentCrawlerPipeline(object):
    def __init__(self):
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user='%s'%db_detail.username,passwd='%s'%db_detail.passwd,db='%s'%db_detail.database_name,charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 
        self.counter=0

    def process_item(self, item, spider):
        self.query="insert into {table_name} (title,year,Show_type,Source,Service,content_type,Added_to_site,Updated_at_DB) values (%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.table)
        self.cursor.execute(self.query,(item['title'],item['year'],item['Show_type'],
                                      item['Source'],item['Service'],item['content_type'],item['Added_to_site'],item['Updated_at_DB']))
        self.counter+=1
        self.connection.autocommit(True)
        print("\n")
        print ("Total commit: ", self.counter)
        print("\n")
        return item
        