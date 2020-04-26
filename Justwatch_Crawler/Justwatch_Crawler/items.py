# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JustwatchCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MovieItem(scrapy.Item):
    movie_id                    = scrapy.Field()
    title                       = scrapy.Field()
    original_title              = scrapy.Field()
    description                 = scrapy.Field()
    release_year                = scrapy.Field()
    ott                         = scrapy.Field()
    credits                     = scrapy.Field()
    rating                      = scrapy.Field() 
    rating                      = scrapy.Field()
    duration                    = scrapy.Field()
    genres                      = scrapy.Field()
    age_rating                  = scrapy.Field()
    provider_id                 = scrapy.Field() 
    service_name                = scrapy.Field() 
    added_to_site               = scrapy.Field()
    updated_at                  = scrapy.Field() 