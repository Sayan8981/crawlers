import scrapy
from scrapy import *
import os
import sys
import hashlib
from hindunews.items import *
#import pdb;pdb.set_trace()
print(sys.path)
import datetime
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class hindunews(Spider):
    
    name="hindunews"
    start_urls=['https://www.thehindu.com/']

    def __init__(self):
        self.national_otherstorycardnews_headlines_url=[]
        self.national_storycardnews_headlines_urls=[]
        self.national_otherstorycardnews_headlines_url=[]
        self.national_news_headlines_urls=[]

    def parse(self,response):
        #import pdb;pdb.set_trace()
        #print (response.body)
        sel=Selector(response)
        url=sel.xpath(xpath.url_xpath).extract()
        print(url)
        for url in url:
        	if "news" in url:
        		news_url=url
        yield Request(news_url, callback=self.parse_news_url,dont_filter=True)

    def parse_news_url(self,news_url):
        print (news_url.url)
        #print (news_url.body) 
        sel=Selector(news_url)
        different_news_urls=sel.xpath(xpath.different_news_xpath).extract()
        print(different_news_urls)
        for urls in different_news_urls:
            #import pdb;pdb.set_trace()
            if '/national' in urls:
                yield Request(url=urls,callback=self.parse_national_news_url,dont_filter=True)
            else:
                print ("The url is not in consideration",urls) 

    def parse_national_news_url(self,national_news_page_url):
        #import pdb;pdb.set_trace()
        if national_news_page_url.url is not None:
            yield Request(url=national_news_page_url.url,callback=self.national_news_headlines_url,dont_filter=True)
        #import pdb;pdb.set_trace()    
        yield Request(url=national_news_page_url.url,callback=self.national_news_pagination,dont_filter=True)

    def national_news_pagination(self,national_news_page_url):
        #import pdb;pdb.set_trace()
        sel=Selector(national_news_page_url)
        self.national_news_nextpage_url=sel.xpath(xpath.news_pagination_xpath).extract()
        if self.national_news_nextpage_url:
            yield Request(url=self.national_news_nextpage_url[0],callback=self.parse_national_news_url,dont_filter=True)    

    def national_news_headlines_url(self,national_news_page_urls):
        #import pdb;pdb.set_trace()
        print("\n")
        print(national_news_page_urls.url)  
        sel=Selector(national_news_page_urls)
        self.national_storycardnews_headlines_urls=sel.xpath(xpath.national_storycard_new_xpath).extract() 
        self.national_otherstorycardnews_headlines_url=sel.xpath(xpath.national_otherstorycard_news_xpath).extract()
        if self.national_storycardnews_headlines_urls or self.national_otherstorycardnews_headlines_url:
            self.national_news_headlines_urls=self.national_storycardnews_headlines_urls+self.national_otherstorycardnews_headlines_url
        for headlines_urls in self.national_news_headlines_urls:
            yield Request(url=headlines_urls,callback=self.national_news_details,dont_filter=True)

    def national_news_details(self,headlines_url):
        #import pdb;pdb.set_trace()
        sel=Selector(headlines_url)
        national_news_item=Hindu_national_newsItem()
        national_news_item['section']='National'
        national_news_item['news_headlines']=sel.xpath(xpath.national_news_headlines_xpath).extract()
        if national_news_item['news_headlines']:
            national_news_item['news_headlines']=''.join(national_news_item['news_headlines']).strip("\n ").encode('ascii','ignore')
        else:
            national_news_item['news_headlines']='None'    
        national_news_item['news_tagline']=sel.xpath(xpath.national_news_tagline_xpath).extract()
        if national_news_item['news_tagline']:
            national_news_item['news_tagline']=national_news_item['news_tagline'][0].strip("\n ").encode('ascii','ignore')  
        else:
            national_news_item['news_tagline']='None'                   
        national_news_item['news_details']=''.join(data for data in sel.xpath(xpath.national_news_details_xpath).extract()).strip(" ").encode('ascii','ignore')
        if national_news_item['news_details']=="":
            national_news_item['news_details']=''.join(data for data in sel.xpath(xpath.national_news_details_alternative_xpath).extract()).strip(" ").encode('ascii','ignore')
        national_news_item['country']=sel.xpath(xpath.national_news_country_xpath).extract()[0].strip("\n,: ").encode("ascii",'ignore')
        national_news_item['news_date']=''.join(sel.xpath(xpath.national_news_date_xpath).extract()).strip("\n ").encode("ascii",'ignore')
        national_news_item['news_updated_at']=''.join(sel.xpath(xpath.national_news_updatedDate_xpath).extract()).strip("\n ").encode("ascii",'ignore')
        national_news_item['news_url']=headlines_url.url
        national_news_item['sk_key']=hashlib.md5(headlines_url.url.encode()).hexdigest()
        national_news_item['dump_updated_at']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield national_news_item




                
                          
                    
                
                
                    
                    
        