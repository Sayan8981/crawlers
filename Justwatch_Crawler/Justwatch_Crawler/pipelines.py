# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Justwatch_Crawler.items import *
import logging
import MySQLdb
import os
import sys
import db_detail

class JustwatchCrawlerPipeline(object):

    def __init__(self):
        self.counter_movies=0
        self.counter_series=0
        self.counter_episode=0

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            self.query="insert into {table_name} (Netflix_id,title,show_type,description,year,rating,duration,season_number,audio,url,available_season,image,genres,Director,Actor,subtitles,added_to_site,content_type,content_history,updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.table)
            self.cursor.execute(self.query,(item["netflix_id"],item["title"],item["show_type"],item["description"],item["year"],item["rating"],item["run_time"],item["season_number"],item["record_language"],item["url"],item["available_season"],item["image"],item["genres"],item["Director"],item["Actor"],item["subtitles"],item["added_to_site"],item["content_type"],item["history"],item["updated_at"]))
            self.connection.autocommit(True)
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

        elif isinstance(item, EpisodeItem):
            self.counter_episode+=1
            logging.info({"Total data count episodes": self.counter_episode})
            logging.info("\n")
            logging.info(item)
            return item
                   
