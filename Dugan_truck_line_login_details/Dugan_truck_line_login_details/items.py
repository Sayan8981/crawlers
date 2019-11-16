# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DuganTruckLineLoginDetailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pro_number=scrapy.Field()
    status=scrapy.Field()
    trip=scrapy.Field()
    bill_of_lading=scrapy.Field()
    pickedup_date=scrapy.Field()
    delivery_date=scrapy.Field()
    ETA=scrapy.Field()
    shipper=scrapy.Field()
    consignee=scrapy.Field()
