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
        self.connection=MySQLdb.connect(host=db_detail.IP_addr,user='%s'%db_detail.username,passwd='%s'%db_detail.passwd,db='%s'%db_detail.database_name,charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor()

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            self.query="insert into {table_name} (Movie_id,Title,Show_type,Description,Release_year,original_title,OTT,Cast,Duration,Genres,Rating,Age_Rating,Service_name,Added_to_site,Updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.movie_table)
            self.cursor.execute(self.query,(item["movie_id"],item["title"],item["show_type"],item["description"],item["release_year"],item["original_title"],item["ott"],item["credits"],item["duration"],item["genres"],item["rating"],item["age_rating"],item["service_name"],item["added_to_site"],item["updated_at"]))
            self.connection.autocommit(True)
            self.counter_movies+=1
            logging.info({"Total data count movies": self.counter_movies})
            logging.info("\n")
            logging.info(item)
            return item

        elif isinstance(item, SeriesItem):
            self.query="insert into {table_name} (Series_id,Season_id,Title,Show_type,Description,Release_year,original_title,Cast,Season_number,Genres,Rating,Age_Rating,Service_name,Added_to_site,Updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.Series_table)
            self.cursor.execute(self.query,(item["series_id"],item["season_id"],item["title"],item["show_type"],item["description"],item["release_year"],item["original_title"],item["credits"],item["season_number"],item["genres"],item["rating"],item["age_rating"],item["service_name"],item["added_to_site"],item["updated_at"]))
            self.connection.autocommit(True)
            self.counter_series+=1
            logging.info({"Total data count series": self.counter_series})
            logging.info("\n")
            logging.info(item)
            return item 

        elif isinstance(item, EpisodeItem):
            self.query="insert into {table_name} (Series_id,Season_id,Episode_id,Series_title,Title,Show_type,Description ,OTT,Duration,season_number,Episode_number,Service_name,Updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name=db_detail.Episodes_table)
            self.cursor.execute(self.query,(item["series_id"],item["season_id"],item["episode_id"],item["series_title"],item["title"],item["show_type"],item["description"],item["ott"],item["duration"],item["season_number"],item["episode_number"],item["service_name"],item["updated_at"]))
            self.connection.autocommit(True)
            self.counter_episode+=1
            logging.info({"Total data count episodes": self.counter_episode})
            logging.info("\n")
            logging.info(item)
            return item
                   
