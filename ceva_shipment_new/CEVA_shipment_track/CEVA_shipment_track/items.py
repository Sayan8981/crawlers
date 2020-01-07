# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CevaShipmentTrackItem(scrapy.Item):
    # define the fields for your item here like:
    waybill_number=scrapy.Field()
    ship_date=scrapy.Field()
    due_date=scrapy.Field()
    estimated_delivery_date=scrapy.Field()
    shipper_location=scrapy.Field()
    consignee_location=scrapy.Field()
    total_pcs=scrapy.Field()
    actual_weight=scrapy.Field()
    charge_weight=scrapy.Field()
    freight_terms=scrapy.Field()
    service_level=scrapy.Field()
    delivery_type=scrapy.Field()
    movement_type=scrapy.Field()

    history_data=scrapy.Field()
