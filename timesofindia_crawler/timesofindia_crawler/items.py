# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TimesofindiaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    state=scrapy.Field()
    news_headlines=scrapy.Field()
    news_details=scrapy.Field()
    city=scrapy.Field()
    news_updated_at=scrapy.Field()
    news_url=scrapy.Field()
    sk_key=scrapy.Field()
    dump_updated_at=scrapy.Field()
    #pass
