import scrapy
from scrapy import *
import os
import sys
import hashlib
from Dugan_truck_line_login_details.items import *
#import pdb;pdb.set_trace()
print(sys.path)
import datetime
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class Dugan_crawler(Spider):

    name='Dugan' 
    start_urls=["http://dublweb.roadvision.com/PublicShipmentSearch.aspx"]

    def __init__(self):
        self.input_id_arr=[]

    def parse(self,response):
        import pdb;pdb.set_trace()        
        input_id=str(input("Enter the id:"))
        self.input_id_arr.append(input_id)
        Sel=Selector(response)
        viewstate=''.join(response.xpath(xpath.viewstate_xpath).extract())
        eventvalidation=''.join(Sel.xpath(xpath.eventvalidation_xpath).extract())
        cookies=response.headers.get('Set-Cookie').decode('utf-8').split(";")[0]
        headers= {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Origin': 'http://dublweb.roadvision.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Referer': 'http://dublweb.roadvision.com/PublicShipmentSearch.aspx',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8,la;q=0.7',
                'Set-Cookie': cookies,
                }
        for id_ in self.input_id_arr:
            data= {
                  'ctl00_ToolkitScriptManager1_HiddenField': '',
                  '__EVENTTARGET': '',
                  '__EVENTARGUMENT': '',
                  '__VIEWSTATE': viewstate,
                  '__EVENTVALIDATION': eventvalidation,
                  'ctl00$ContentPlaceHolder1$txtProNum': id_,
                  'ctl00$ContentPlaceHolder1$txtBOL': '',
                  'ctl00$ContentPlaceHolder1$cmdSubmit': 'Search',
                  'ctl00$ContentPlaceHolder1$txtCarrierPro': '',
                  'ctl00$ContentPlaceHolder1$txtPONum': ''
                }    
        yield FormRequest(url=response.url,method='POST',headers=headers,formdata=data
                                     ,callback=self.extract_data,dont_filter=True)

    def extract_data(self,response):
        
        import pdb;pdb.set_trace()
        print (response.body)
        item=DuganTruckLineLoginDetailsItem()

        item["pro_number"]=''.join(response.xpath(xpath.pro_number_xpath).extract())
        item["status"]=response.xpath(xpath.status_xpath).extract_first().replace('&nbsp','').strip()
        item["trip"]=response.xpath(xpath.trip_xpath).extract()[2].split("TRIP")[1].strip()
        item["bill_of_lading"]=''.join(response.xpath(xpath.bill_of_lading_xpath).extract())
        item["pickedup_date"]=''.join(response.xpath(xpath.pickedup_date_xpath).extract())
        item["delivery_date"]=''.join(response.xpath(xpath.delivery_date).extract())
        item["ETA"]=''.join(response.xpath(xpath.eta_xpath).extract()) 
        item["shipper"]=''.join(response.xpath(xpath.shipper_name_xpath).extract())+" ,"+''.join(response.xpath(xpath.shipper_addr_xpath).extract())+" ,"+' '.join(response.xpath(xpath.shipper_city_xpath).extract())+" ,"+' '.join(response.xpath(xpath.shipper_state_xpath).extract())+" ,"+' '.join(response.xpath(xpath.shipper_zip_xpath).extract())
        item["consignee"]=''.join(response.xpath(xpath.consignee_name_xpath).extract())+','+''.join(response.xpath(xpath.consignee_addr_xpath).extract())+','+''.join(response.xpath(xpath.consignee_state_xpath).extract())+','+''.join(response.xpath(xpath.consignee_city_xpath).extract())+','+''.join(response.xpath(xpath.consignee_zip_xpath).extract())
        data_= ''.join(Sel.xpath('//tr[@style="text-decoration: overline;"]/td/text()').extract())
        import pdb;pdb.set_trace()
        yield item         



"""
sample input:
4114310
4114358
4114363
4114351
4114345
4114355
4114373
"""
