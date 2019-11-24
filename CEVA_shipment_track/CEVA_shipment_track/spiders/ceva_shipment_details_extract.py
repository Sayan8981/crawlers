import scrapy
from scrapy import *
import os
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
        self.history_event_key=[]
        self.history_data_column=[]=''
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
        item["waybill_number"]=''.join(response.xpath('//td[contains(text(),"Waybill Number:")]/following-sibling::td/text()').extract())
        item["ship_date"]=''.join(response.xpath('//td[contains(text(),"Ship Date:")]/following-sibling::td/text()').extract())
        item["due_date"]=''.join(response.xpath('//td[contains(text(),"Due Date:")]/following-sibling::td/text()').extract())
        item["estimated_delivery_date"]=''.join(response.xpath('//td[contains(text(),"Estimated Delivery Date:")]/following-sibling::td/text()').extract())
        item["shipper_location"]=''.join(response.xpath('//td[contains(text(),"Shipper Location")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()
        item["consignee_location"]=''.join(response.xpath('//td[contains(text(),"Consignee Location")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()

        item["total_pcs"]=''.join(response.xpath('//td[contains(text(),"Total Pieces:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()
        item["actual_weight"]=''.join(response.xpath('//td[contains(text(),"Actual Weight:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()
        item["charge_weight"]=''.join(response.xpath('//td[contains(text(),"Charge Weight:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()

        item["freight_terms"]=''.join(response.xpath('//td[contains(text(),"Freight Terms:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()
        item["service_level"]=''.join(response.xpath('//td[contains(text(),"Service Level:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()
        item["delivery_type"]=''.join(response.xpath('//td[contains(text(),"Delivery Type:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()
        item["movement_type"]=''.join(response.xpath('//td[contains(text(),"Movement Type:")]/following-sibling::td/text()').extract()).replace('\xa0',' ').replace("\t","").replace("\n","").replace("\r","").strip()

        self.history_event_key=response.xpath('//td[contains(@class,"portlet-table-header")]/text()').extract()[0:5]
        self.history_data_column=response.xpath('//table[tr[td[contains(text(),"Key Event History")]]]/following-sibling::table[2][@border="0"]/tr/td[1]/text()').extract()

        for data in self.history_data_column:
            self.signature_remarks=','.join(response.xpath("//td[text()='%s']/following-sibling::td/a/text()"%data).extract()).replace('\xa0','').replace("\t",'').replace("\n",'').replace("\r",'').strip(", ")
            if self.signature_remarks!='':
                item["history_data"].append({data:','.join(response.xpath("//td[text()='%s']/following-sibling::td/text()"%data).extract()).replace('\xa0','').replace("\t",'').replace("\n",'').replace("\r",'').strip(", ").split(",")+[self.signature_remarks]})
            else:
                item["history_data"].append({data:','.join(response.xpath("//td[text()='%s']/following-sibling::td/text()"%data).extract()).replace('\xa0','').replace("\t",'').replace("\n",'').replace("\r",'').strip(", ").split(",")})
        yield item 


"""
**
Sample input:

["EC90009356","EC90009210","EC90008803","EC90009014","EC90008855","EC90009003"]
"""