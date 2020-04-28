# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Justwatch_Crawler.items import *
import logging

class JustwatchCrawlerPipeline(object):

    def __init__(self):
        self.counter_movies=0
        self.counter_series=0

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            self.counter_movies+=1
            logging.info({"Total data count movies": self.counter_movies})
            logging.info("\n")
            logging.info(item)
            return item

        elif isinstance(item, SeriesItem):
            self.counter_series+=1
            logging.info({"Total data count series": self.counter_series})
            logging.info("\n")
            logging.info(item)
            return item    
