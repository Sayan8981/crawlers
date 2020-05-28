# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UsaNewonNetflixItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    netflix_id=scrapy.Field()
    title=scrapy.Field()
    show_type=scrapy.Field()
    description=scrapy.Field()
    year=scrapy.Field()
    rating=scrapy.Field()
    run_time=scrapy.Field()
    season_number=scrapy.Field()
    record_language=scrapy.Field()
    url=scrapy.Field()
    available_season=scrapy.Field()
    image=scrapy.Field()
    genres=scrapy.Field()
    Director=scrapy.Field()
    Actor=scrapy.Field()
    subtitles=scrapy.Field()
    added_to_site=scrapy.Field()
    content_type=scrapy.Field()
    history=scrapy.Field()
    updated_at=scrapy.Field()
    
