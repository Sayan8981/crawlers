# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html




import scrapy


class VultureHuluItem(scrapy.Item):
     title = scrapy.Field()
    year=scrapy.Field()
    content_category = scrapy.Field()
    content_available=scrapy.Field()
    content_defination = scrapy.Field()
    updated_db = scrapy.Field()
    service = scrapy.Field()

