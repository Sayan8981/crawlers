# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#import pdb;pdb.set_trace()
import MySQLdb
#import mysql.connector
import os
import sys

class HindunewsPipeline(object):
    def __init__(self):
        #import pdb;pdb.set_trace()
        print ("Enter your database username again.....")
        user=input(str)
        print("Enter your database password again....")
        passwd=input(str)
        self.connection=MySQLdb.connect(host="localhost",user=user,passwd=passwd,db="Hindunews",charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 
        self.counter=0

    def process_item(self, item, spider):
        if item['section']=='National':
            #print (item)
            self.query="insert into National_news_details (sk_key,News_headlines,News_intro,News_details,Country,Date,Updated_at,News_url) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(self.query,(item['sk_key'],item['news_headlines'],item['news_tagline'],item['news_details'],
                                          item['country'],item['date'],item['updated_at'],item['news_url']))
            self.counter+=1
            self.connection.autocommit(True)
            print("\n")
            print ("Total commit: ", self.counter)
            print("\n")
            return item
        self.connection.close()    
