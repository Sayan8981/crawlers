# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import os
import sys

class CevaShipmentTrackPipeline(object):
    def __init__(self):
        #import pdb;pdb.set_trace()
        print ("Enter your database username again.....")
        user=input(str)
        print("Enter your database password again....")
        passwd=input(str)
        self.connection=MySQLdb.connect(host="localhost",user=user,passwd=passwd,db="Ceva_shipment",charset="utf8", use_unicode=True)
        self.cursor=self.connection.cursor() 
        self.counter=0

    def process_item(self, item, spider):
        #import pdb;pdb.set_trace()
        self.query="insert ignore into ceva_shipment_detail (waybill_number,ship_date , due_date , estimated_delivery_date , shipper_location ,consignee_location ,total_pcs , actual_weight ,charge_weight , freight_terms , service_level , delivery_type ,movement_type ,history_data) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        self.cursor.execute(self.query,(item["waybill_number"],item["ship_date"],item["due_date"],item["estimated_delivery_date"],item["shipper_location"],item["consignee_location"],item["total_pcs"],item["actual_weight"],item["charge_weight"],item["freight_terms"],item["service_level"],item["delivery_type"],item["movement_type"],str(item["history_data"])))
        self.counter+=1
        self.connection.autocommit(True)
        print("\n")
        print ("Total commit: ", self.counter)
        print("\n")
        return item
        self.connection.close()
        