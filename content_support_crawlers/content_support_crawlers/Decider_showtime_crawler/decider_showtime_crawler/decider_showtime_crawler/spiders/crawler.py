import scrapy 
from scrapy import *
import sys
import os
import time,re
import pinyin,unidecode
from scrapy import signals
from datetime import datetime,timedelta
from decider_showtime_crawler.items import *
sys.path.insert(0,os.getcwd()+'/xpath')
sys.path.insert(1,os.getcwd()+'/operation')
import create_db_tables
import xpath
import db_output
from db_output import db_output_stats
from send_mail import send_emails


class decidershowtimebrowse(Spider):

    name="decidershowtimebrowse"
    start_urls=["https://decider.com/article/new-on-showtime/"]
    """["https://decider.com/%s/new-on-showtime-%s/"%(datetime.now().strftime('%Y/%m/%d'),datetime.now().strftime('%B-%Y').lower())]"""

    #initialization:
    def __init__(self):
        self.content_title=''
        self.service=''
        self.ET_PT_timing=''
        self.content_category=''
        self.content_defination=''
        self.content_released='None'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(decidershowtimebrowse, cls).from_crawler(crawler, *args, **kwargs)
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
        self.ET_PT_timing=''
        self.content_category=''
        self.content_defination=''
        self.content_released='None'
        self.service=''

    def parse(self,response):
        yield Request(url=response.url,callback=self.content_scraped,dont_filter = True)
    
    #TODO: data field to scrape 
    def content_scraped(self,response):
        sel=Selector(response)
        #TODO: first take all titles from the coming page
        extract_titles=sel.xpath(xpath.title_xpath).extract()
        #TODO: Iterate through title to get the mata data for particular title 
        for title in extract_titles:
            self.cleanup()
            self.content_title=unidecode.unidecode(pinyin.get(title)).strip(' ')
            if self.content_title!='':
                title=pinyin.get(title.replace('\"','\''))
                title=re.sub(re.compile("'.*'?"),"",title).strip(' ')
                self.ET_PT_timing=sel.xpath(xpath.ET_PT_xpath%title).extract_first().strip('\n').strip('(').strip(')').replace(')','')
                self.content_category="".join(sel.xpath(xpath.category_xpath%title).extract()[-1:])
                if 'Series' not in self.content_category and 'Streaming' not in self.content_category and 'Sports' not in self.content_category:
                    self.content_released=''.join(sel.xpath(xpath.content_release_xpath%title).extract()[-1:])
                elif 'Series' not in self.content_category and 'Sports' not in self.content_category:
                    self.content_defination =''.join(sel.xpath(xpath.content_release_xpath%title).extract()[-1:])      
                self.content_released=self.content_released.replace('Released ','')        
                self.service="Showtime"
                print({"content_title":self.content_title,"content_category":self.content_category,"content_released":self.content_released,"content_defination":self.content_defination,"page_url":response.url})
                yield Request(url=response.url,meta={"content_title":self.content_title,"content_category":self.content_category,"content_released":self.content_released,"content_defination":self.content_defination,"page_url":response.url,"service":self.service,"ET_PT_timing":self.ET_PT_timing},callback=self.item_stored,dont_filter=True)      

    def item_stored(self,response): 
        item=DeciderCrawlerItem()
        item["title"]=response.meta["content_title"]
        item["content_category"]=response.meta["content_category"]
        item["content_released"]=response.meta["content_released"]
        item["content_defination"]=response.meta["content_defination"]
        item["ET_PT_timing"]=response.meta["ET_PT_timing"]
        item["updated_db"]=datetime.now().strftime('%b %d, %Y')
        item["service"]=response.meta["service"]
        yield item
        
           
