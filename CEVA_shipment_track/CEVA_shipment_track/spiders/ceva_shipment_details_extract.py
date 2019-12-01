"""*Saayan"""

import scrapy
from scrapy import *
import os
import re
import sys
import hashlib
from CEVA_shipment_track.items import *
#import pdb;pdb.set_trace()
print(sys.path)
import datetime
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class CEVA_shipment_track(Spider):

    name="ceva_shipment"
    start_urls=["https://etracking.cevalogistics.com/eTracking.aspx?uid="]

    def __init__(self):
        self.input_id=["EC90009356","EC90009210","EC90008803","EC90009014","EC90008855","EC90009003"]
        self.history_data_column=[]
        self.signature_remarks=''
     
    def parse(self,response):
        #import pdb;pdb.set_trace()
        self.viewstate=response.xpath(xpath.viewstate_xpath).extract()[0]
        self.viewstategenerator=''.join(response.xpath(xpath.viewstategenerator_xpath).extract())
        cookies=response.headers.get('Set-Cookie').decode('utf-8').split(";")[0]
        headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'https://etracking.cevalogistics.com',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',    
                'Sec-Fetch-User': '?1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Referer': self.start_urls[0],
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8,la;q=0.7',
                'Set-Cookie':cookies,
                 }

        for _id in self.input_id: 
            data = {
                      '__EVENTTARGET': '',
                      '__EVENTARGUMENT': '',
                      '__LASTFOCUS': '',
                      '__VIEWSTATE': self.viewstate,
                      '__VIEWSTATEGENERATOR': self.viewstategenerator,
                      'ModeList': '1',
                      'lstbasics': 'House Waybill',
                      'txtairWayBillNumber': _id,
                      'btnSearch': 'Track'
                    }         

            yield FormRequest(url=response.url,method='POST',headers=headers,formdata=data
                                     ,callback=self.extract_data,dont_filter=True)


    def extract_data(self,response):
        #import pdb;pdb.set_trace()
        #print (response.body) 
        item=CevaShipmentTrackItem()
        item["history_data"]=[]
        item["waybill_number"]=''.join(response.xpath(xpath.waybill_number_xpath).extract())
        item["ship_date"]=''.join(response.xpath(xpath.ship_date_xpath).extract())
        item["due_date"]=''.join(response.xpath(xpath.due_date_xpath).extract())
        item["estimated_delivery_date"]=''.join(response.xpath(xpath.estimated_delivery_date_xpath).extract())
        item["shipper_location"]=' '.join(re.findall("[\w,]+",''.join(response.xpath(xpath.shipper_location_xpath).extract())))
        item["consignee_location"]=' '.join(re.findall("[\w,]+",''.join(response.xpath(xpath.consignee_location_xpath).extract())))

        item["total_pcs"]=''.join(response.xpath(xpath.totalpcs_xpath).extract())
        item["actual_weight"]=' '.join(re.findall("[\w,./]+",''.join(response.xpath(xpath.actual_weight_xpath).extract())))
        item["charge_weight"]=' '.join(re.findall("[\w,./]+",''.join(response.xpath(xpath.charge_weight_xpath).extract())))

        item["freight_terms"]=''.join(response.xpath(xpath.freight_terms_xpath).extract())
        item["service_level"]=''.join(response.xpath(xpath.service_level_xpath).extract())
        item["delivery_type"]=''.join(response.xpath(xpath.delivery_type_xpath).extract())
        item["movement_type"]=' '.join(re.findall("[\w,]+",''.join(response.xpath(xpath.movement_type_xpath).extract())))

        self.history_event_key=response.xpath('//td[contains(@class,"portlet-table-header")]/text()').extract()[1:5]
        self.history_data_column=response.xpath(xpath.history_data_column_xpath).extract()

        for data in self.history_data_column:
            self.signature_remarks=','.join(response.xpath(xpath.signature_remarks%data).extract())
            item["history_data"].append({data:dict(zip(self.history_event_key,re.findall("[\w:-]+",','.join(response.xpath(xpath.history_data%data).extract()))+[self.signature_remarks]))})

        #print(item)        
        yield item 


"""
**
Sample input:

["EC90009356","EC90009210","EC90008803","EC90009014","EC90008855","EC90009003"]
"""