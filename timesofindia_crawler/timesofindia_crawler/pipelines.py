# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
#import mysql.connector
import os
import sys
from timesofindia_crawler import create_db_tables

class TimesofindiaCrawlerPipeline(object):
    def __init__(self):
        self.connection=MySQLdb.connect(host="localhost",user='root',passwd='root@123',db="TOI_news",charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 
        self.counter=0

    def process_item(self, item, spider):
        #import pdb;pdb.set_trace()
        self.query="insert into TOI_news_details (sk_key, News_headlines, News_details, State,City ,Dump_updated,News_Updated, News_url) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(self.query,(item['sk_key'],item['news_headlines'],item['news_details'],
                                      item['state'],item['city'],item['dump_updated_at'],item['news_updated_at'],item['news_url']))
        self.counter+=1
        self.connection.autocommit(True)
        print("\n")
        print ("Total commit: ", self.counter)
        print("\n")
        return item
        self.connection.close()
