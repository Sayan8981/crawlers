import scrapy
from scrapy import *
import os
import sys
import hashlib
#from CevaShipmentTrackItem.items import *
#import pdb;pdb.set_trace()
print(sys.path)
import datetime
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class CEVA_shipment_track(Spider):

    name="ceva_shipment"
    start_urls=["https://etracking.cevalogistics.com/eTracking.aspx?uid="]

    def __init__(self):
        self.input_array=[]
     
    def parse(self,response):
        input_id=str(input("Enter the bill number:"))
        self.input_array.append(input_id)
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

        for _id in self.input_array: 
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
        import pdb;pdb.set_trace()
        print (response.body)    














"""
ceva,EC90008855
ceva,EC90009003
ceva,EC90009014
ceva,EC90008803
ceva,EC90009210
ceva,EC90009356
"""