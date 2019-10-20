# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Hindu_national_newsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_headlines=scrapy.Field()
    news_tagline=scrapy.Field()
    news_details=scrapy.Field()
    country=scrapy.Field()
    date=scrapy.Field()
    updated_at=scrapy.Field()
    news_url=scrapy.Field()
