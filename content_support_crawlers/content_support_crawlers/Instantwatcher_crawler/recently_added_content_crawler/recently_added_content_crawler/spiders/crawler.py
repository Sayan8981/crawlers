import scrapy 
from scrapy import *
import sys
import os
import time
import pinyin,unidecode
from scrapy import signals
from datetime import datetime,timedelta
from recently_added_content_crawler.items import *
sys.path.insert(0,os.getcwd()+'/xpath')
sys.path.insert(1,os.getcwd()+'/operation')
import create_db_tables
import xpath
import db_output
from db_output import db_output_stats
from send_mail import send_emails


class instantwatcherbrowse(Spider):

    name="instantwatcherbrowse"
    start_urls=["https://instantwatcher.com"]

    #initialization:
    def __init__(self):
        self.content_type_key=[]
        self.source_url=''
        self.provider_name=''
        self.title_array_prev_dates=[]
        self.require_date=''
        self.all_title_array=[]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(instantwatcherbrowse, cls).from_crawler(crawler, *args, **kwargs)
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
        self.all_title_array=[]    
        self.title_array_prev_dates=[]
        self.content_type_key=[]
        self.all_year=[]
        self.all_year_prev_dates=[]
        self.year_array=[]

    def parse(self,response):
        sel=Selector(response)
        source_node=sel.xpath(xpath.source_node).extract()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8,la;q=0.7',
        } 
        for source in source_node:
            if source.lower()== "amazon":  
                self.source_url=''.join(sel.xpath(xpath.source_url_xpath%source).extract())
                yield Request(url=''.join(self.start_urls)+self.source_url,meta={'source_name':source},
                                        headers=headers,callback=self.parse_url,dont_filter = True) 

    def parse_url(self,response):
        self.provider_name=response.meta['source_name']
        section=response.xpath(xpath.section_xpath%response.meta['source_name']).extract()
        section_url=response.xpath(xpath.section_urls%response.meta['source_name']).extract()
        source_section_wise_url=dict(zip(section,section_url))
        if self.provider_name=='Amazon':
            for sections in section:
                if sections=="New Prime":
                    yield Request(url=''.join(self.start_urls)+source_section_wise_url[sections]
                                    ,meta={"service":sections},callback=self.parse_amazon_content,dont_filter=True)
                elif sections=="New Rental":
                    yield Request(url=''.join(self.start_urls)+source_section_wise_url[sections]
                                    ,meta={"service":sections},callback=self.parse_amazon_content,dont_filter=True)
                elif sections=="Purchase":
                    yield Request(url=''.join(self.start_urls)+source_section_wise_url[sections]
                                    ,meta={"service":sections},callback=self.parse_amazon_content,dont_filter=True)    

    def parse_amazon_content(self,response):
        content_type=response.xpath(xpath.checked_content_type_xpath).extract()[1:]
        for content in content_type:
            self.content_type_key.append(''.join(response.xpath(xpath.checked_content_type_key_xpath%content).extract()))
        dict_content_type_key=dict(zip(content_type,self.content_type_key))
        for key,value in dict_content_type_key.items():
            content_url=response.url.replace('1+2','%s'%value)
            yield Request(url=content_url,meta={'content_type':key,"service":response.meta["service"]}
                                                               ,callback=self.pagination,dont_filter=True)

    def pagination(self,response):
        if self.provider_name=='Amazon':
            if response.meta["content_type"].lower() == 'movies':
                yield Request(url=response.url,meta={"content_type":response.meta["content_type"],
                               "service":response.meta["service"]},callback=self.call_next_page,dont_filter=True)
            else:
                yield Request(url=response.url,meta={"content_type":response.meta["content_type"],
                               "service":response.meta["service"]},callback=self.call_next_page,dont_filter=True)


    def call_next_page(self,response):
        yield Request(url=response.url,meta={"content_type":response.meta["content_type"],
                       "service":response.meta["service"]},callback=self.content_scraped,dont_filter=True)
        next_page_url="{}{}{}{}".format(''.join(self.start_urls),self.source_url,'/search',''.join(response.xpath(xpath.next_page).extract()))
        if next_page_url is not None:
            if next_page_url !="{}{}{}".format(''.join(self.start_urls),self.source_url,'/search'):
                yield Request(url=next_page_url,meta={"content_type":response.meta["content_type"],
                      "service":response.meta["service"]},callback=self.pagination,dont_filter=True)                              
            
    def content_scraped(self,response):
        #fields to scrape
        self.cleanup()
        sel=Selector(response)
        self.require_date=(datetime.now() - timedelta(days=1)).strftime('%b %d, %Y')
        date_node=sel.xpath('//h4/text()').extract()
        if len(date_node)>1:
            for date in date_node:
                if date==self.require_date:
                    self.all_title_array=sel.xpath(xpath.title_xpath%str(date)).extract()
                    for all_title in self.all_title_array:
                        try:
                            if unidecode.unidecode(pinyin.get(sel.xpath(xpath.year_xpath%(str(date),str(all_title).replace('"',''))).extract_first())) is not None:
                                self.all_year.append(sel.xpath(xpath.year_xpath%(str(date),str(all_title).replace('"',''))).extract_first())
                            else:
                                self.all_year.append('')
                        except Exception as error:
                            self.all_year.append('')            
                else:
                    self.title_array_prev_dates+=sel.xpath(xpath.title_xpath%str(date)).extract()
                    for title_prev_date in self.title_array_prev_dates:
                        try:
                            if unidecode.unidecode(pinyin.get(sel.xpath(xpath.year_xpath%(str(date),str(title_prev_date).replace('"',''))).extract_first())) is not None:
                                self.all_year_prev_dates.append(sel.xpath(xpath.year_xpath%(str(date),str(title_prev_date).replace('"',''))).extract_first())
                            else:
                                self.all_year_prev_dates.append('')
                        except Exception as error:
                            self.all_year_prev_dates.append('')         
            title_array_year=list(set(zip(self.all_title_array,self.all_year))-set(zip(self.title_array_prev_dates,self.all_year_prev_dates)))
            if title_array_year:
                yield Request(url=response.url,meta={"title_array_with_year":title_array_year,"content_type":response.meta["content_type"],"service":response.meta["service"]},callback=self.item_stored,dont_filter=True)
        else:
            title_array=sel.xpath(xpath.title_xpath%self.require_date).extract()
            for title in title_array:
                try:
                    if unidecode.unidecode(pinyin.get(sel.xpath(xpath.year_xpath%(self.require_date,str(title).replace('"',''))).extract_first())) is not None:
                        self.year_array.append(sel.xpath(xpath.year_xpath%(self.require_date,str(title).replace('"',''))).extract_first())
                    else:
                        self.year_array.append('')
                except Exception as error:
                    self.year_array.append('')    
            if title_array:
                yield Request(url=response.url,meta={"title_array_with_year":list(set(zip(title_array,self.year_array))),"content_type":response.meta["content_type"],"service":response.meta["service"]},callback=self.item_stored,dont_filter=True)


    def item_stored(self,response): 
        for title in response.meta["title_array_with_year"]:
            item=RecentContentCrawlerItem()
            try:
               item["title"]=str(unidecode.unidecode(pinyin.get(title[0])))
               item["year"]=str(unidecode.unidecode(title[1]))
            except Exception:
               item["title"]=str(title[0])
               item["year"]=str(title[1])
            if response.meta["content_type"].lower()=='movies':
                item["Show_type"]='MO'
            else:
                item["Show_type"]='TVSeason'    
            item["Source"]=self.provider_name
            item["Service"]=response.meta["service"]
            item["content_type"]='Recently_Added'
            item["Added_to_site"]=self.require_date
            item["Updated_at_DB"]=datetime.now().strftime('%b %d, %Y') 
            print ("\n") 
            print ("Crawling ....",item["Updated_at_DB"])
            print (item)
            yield item    
             
                    
        
           
