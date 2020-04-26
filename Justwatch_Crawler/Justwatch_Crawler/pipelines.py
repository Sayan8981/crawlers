# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Justwatch_Crawler.items import *
import logging

class JustwatchCrawlerPipeline(object):

    def __init__(self):
        self.counter=0

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            self.counter+=1
            logging.info({"Total data count ": self.counter})
            return item
