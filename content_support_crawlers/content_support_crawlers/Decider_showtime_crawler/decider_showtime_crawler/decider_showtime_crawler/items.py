# -*- coding: utf-8 -*-

# Define here the models for your scraped items

import scrapy


class DeciderCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title=scrapy.Field()
    content_category=scrapy.Field()
    content_released=scrapy.Field()
    content_defination=scrapy.Field()
    updated_db=scrapy.Field()
    service=scrapy.Field()
    ET_PT_timing=scrapy.Field()



