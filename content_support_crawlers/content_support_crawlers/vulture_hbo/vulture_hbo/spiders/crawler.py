import scrapy 
from scrapy import *
import sys
import os
import time,re
import pinyin,unidecode
from scrapy import signals
from datetime import datetime,timedelta
from vulture_hbo.items import *
sys.path.insert(0,os.getcwd()+'/xpath')
sys.path.insert(1,os.getcwd()+'/operation')
import create_db_tables
import db_output
from db_output import db_output_stats
from send_mail import send_emails
import re

class vulturehbobrowse(Spider):

    name="vulturehbobrowse"
    start_urls=["https://www.vulture.com/article/new-on-hbo-movies-shows-originals.html"]

    #initialization:
    def __init__(self):
        self.content_title=''
        self.year=''
        self.service=''
        self.content_category=''
        self.content_available='None'
        self.content_defination=''

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(vulturehbobrowse, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    #TODO: to get the signal when spider closing
    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
        # Whatever is here will run when the spider is done.
        print ("Preparing to create csv file from database...............")
        db_output_stats().main()
        time.sleep(10)
        print("Preparing to send email to client.................")
        send_emails().main()

    def cleanup(self):
        self.content_title=''
        self.year=''
        self.content_category='Movie'
        self.content_available='None'
        self.service='HBO'
        self.content_defination=''

    def parse(self,response):
        yield Request(url=response.url,callback=self.content_scraped,dont_filter = True)

    #TODO: data field to scrape 
    def content_scraped(self,response):
        sel=Selector(response)
        #TODO: first take all titles from the coming page
        date_nodes = date_nodes = response.xpath('//h2[contains(@class,"clay-subheader")] | p[contains(@class,"clay-paragraph")]')
        for x in date_nodes:
            self.cleanup()
            date = unidecode.unidecode(pinyin.get(' '.join(x.xpath('.//text()').extract()).strip().replace('\n', '')))
            if 'Available ' not in date: continue
            title_node = x.xpath('.//following-sibling::p')[0]
            if '<br>' not in title_node.extract().encode('utf-8'):
                title = ''.join(title_node.xpath('.//text() | .//em//text()').extract())
                self.content_title = unidecode.unidecode(pinyin.get(title))
                self.content_titles = self.get_content_title()
                self.content_available=date.replace("Available ",'')
                yield Request(url=response.url,meta={"content_title":self.content_title,"year":self.year,"content_category":self.content_category,"content_available":self.content_available,"content_defination":self.content_defination,"page_url":response.url,"service":self.service},callback=self.item_stored,dont_filter=True)
            else:
                if '<br>'  in title_node.extract():
                    t_titles = title_node.xpath('.//text() | .//em//text()').extract()
                    for title in set(t_titles):
                        self.content_title =  unidecode.unidecode(pinyin.get(title))
                        self.content_titles = self.get_content_title()
                        self.content_available=date.replace("Available ",'')
                        yield Request(url=response.url,meta={"content_title":self.content_title,"year":self.year,"content_category":self.content_category,"content_available":self.content_available,"content_defination":self.content_defination,"page_url":response.url,"service":self.service},callback=self.item_stored,dont_filter=True)


    def get_content_title(self):
        if 'Series' in self.content_title or 'Season' in self.content_title or 'Docuseries' in self.content_title:
            self.content_category='TvShow'
        elif 'HBO Original' in self.content_title:
            self.content_defination='HBO Original'
        else:
            self.year = ''.join(re.findall('\d{4}',self.content_title))
            self.content_title=self.content_title.replace(self.year,'').replace(',','')
        return self.content_title





    def item_stored(self,response):
        item=VultureHboItem()
        item["title"]=response.meta["content_title"]
        item["year"]=response.meta["year"]
        item["content_category"]=response.meta["content_category"]
        item["content_available"]=response.meta["content_available"]
        item["content_defination"]=response.meta["content_defination"]
        item["updated_db"]=datetime.now().strftime('%b %d, %Y')
        item["service"]=response.meta["service"]
        yield item

