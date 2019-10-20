# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pdb;pdb.set_trace()
import MySQLdb
import os
import sys
sys.path.insert(0,os.getcwd()+'/user_passwd_config')
import user_passwd_config


class HindunewsPipeline(object):
    def __init__(self):
        #super(CrawlerPipeline, self).__init__(self)
        self.connection=MySQLdb.connect(host="localhost",user=user_passwd_config.username,passwd=user_passwd_config.passwd,db="Hindunews",charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 

    def process_item(self, item, spider):
        if item['section']=='National':
            print (item)
            return item
