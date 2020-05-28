import scrapy 
from scrapy import *
import sys
import os
import time
import pinyin,unidecode
from scrapy import signals
from datetime import datetime,timedelta
from USA_NewOn_Netflix.items import *
sys.path.insert(0,os.getcwd()+'/xpath')
sys.path.insert(1,os.getcwd()+'/operation')
import create_db_tables
import xpath
import db_output
from db_output import db_output_stats
from send_mail import send_emails

#To crawl Netflix USA recent content from the site 

class usanewonnetflix(Spider):
    handle_httpstatus_list = [403,400]
    name="usanewonnetflix"
    start_urls=["https://usa.newonnetflix.info/"]

    #initialization:
    def __init__(self):
        self.history_dict=dict()
        self.url=''
        self.year=''
        self.cast=''
        self.rating=''
        self.genres=''
        self.title=''
        self.duration=''
        self.director=''
        self.content_id=0
        self.content_img=''
        self.content_type=''
        self.added_to_site=''
        self.season_number=0
        self.subtitles='None'
        self.show_type='Null'
        self.record_language=''
        self.available_season=''
        self.content_description=''

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(usanewonnetflix, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    #TODO: to get the signal when spider closing and do rest task
    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
        # Whatever is here will run when the spider is done.
        print ("Preparing to create csv file from database...............")
        db_output_stats().main()
        time.sleep(10)
        print("Preparing to send email to client.................")
        send_emails().main()    

    #TODO: cleanup all the initials 
    def cleanup(self):
        self.history_dict=dict()
        self.url=''
        self.year=''
        self.cast=''
        self.rating=''
        self.genres=''
        self.title=''
        self.duration=''
        self.director=''
        self.content_id=0
        self.content_img=''
        self.content_type=''
        self.added_to_site=''
        self.season_number=0
        self.subtitles='None'
        self.show_type='Null'
        self.record_language=''
        self.available_season=''
        self.content_description=''

    def parse(self,response):
        yield Request(url=response.url,callback=self.parse_url,dont_filter = True)

    #TODO: To parse main url
    def parse_url(self,response):
        sel=Selector(response)
        extract_content_urls=sel.xpath(xpath.content_urls_xpath).extract()
        for urls in extract_content_urls:
            content_url='{}{}'.format(self.start_urls[0],urls)
            yield Request(url=content_url,callback=self.content_scraped,dont_filter=True)
    
    #TODO: Fields to extarct from site 
    def content_scraped(self,response):
        self.cleanup()
        sel=Selector(response)
        self.title=''.join(response.xpath(xpath.title_xpath).extract_first().split(':')[:1])
        self.url=sel.xpath(xpath.url_xpath).extract_first()
        if self.url!='':
            self.content_id=self.url.split('/')[-1:][0]
        self.content_type=sel.xpath(xpath.content_type_xpath).extract_first() 
        self.genres=sel.xpath(xpath.genre_xpath).extract_first().replace('Films Based on ','')   
        self.content_img=response.xpath(xpath.img_xpath).extract_first()
        history_tags=response.xpath(xpath.history_tags_xpath).extract()
        if history_tags:
            for history in history_tags:
                if self.title not in history:
                    try:
                        self.history_dict[response.xpath(xpath.key_xpath%history).extract_first().strip()]=str(history)
                    except Exception:
                        pass
        tag_nodes =sel.xpath(xpath.other_details_xpath).extract()
        for node in tag_nodes:
            if node!='':
                if 'date added' in node.lower():
                    self.added_to_site= sel.xpath(xpath.date_xpath%node).extract_first()
                    if self.added_to_site is not None:
                        self.added_to_site=self.added_to_site.strip()
                elif 'description' in node.lower():
                    self.content_description=unidecode.unidecode(pinyin.get(sel.xpath(xpath.description_xpath%node).extract_first())).strip()    
                elif 'certificate' in node.lower():
                    self.rating=sel.xpath(xpath.rating_xpath%node).extract_first()
                elif 'year' in node.lower():
                    self.year=sel.xpath(xpath.year_xpath%node).extract_first().replace(' ','')    
                elif 'duration' in node.lower():
                    self.duration=sel.xpath(xpath.duration_xpath%node).extract_first().strip()
                    if 'Seasons' in self.duration or 'Season' in self.duration or 'Limited' in self.duration:
                        self.season_number=self.duration.replace(' Seasons','').replace(' Season','').replace(' Series','')
                        self.duration=0
                        self.show_type="TvSeries"
                    else:
                        self.show_type="Movie"    
                elif 'audio' in node.lower():
                    self.record_language=sel.xpath(xpath.record_lang_xpath%node).extract_first().strip()
                elif 'subtitles' in node.lower():
                    self.subtitles=sel.xpath(xpath.subtitles_xpath%node).extract_first().strip()        
                elif 'director' in node.lower():
                    self.director=','.join(sel.xpath(xpath.director_xpath%node).extract())
                elif 'cast' in node.lower():
                    self.cast=','.join(response.xpath(xpath.cast_xpath%node).extract())
                elif 'available seasons' in node.lower():
                    self.available_season= sel.xpath(xpath.available_season_xpath%node).extract_first().strip()   
        yield Request(url=response.url,meta={"id":self.content_id,"title":self.title,"show_type":self.show_type,"description":self.content_description,"year":self.year,"rating":self.rating,"duration":self.duration,"season_number":self.season_number,"audio":self.record_language,"url":self.url,"image":self.content_img,"genres":self.genres,"Director":self.director,"Actor":self.cast,"subtitles":self.subtitles,"added_to_site":self.added_to_site,"content_type":self.content_type,"content_history":self.history_dict,"available_season":self.available_season},callback=self.item_stored,dont_filter=True)                   

    #TODO: Items sending to DB through pipeline
    def item_stored(self,response): 
        item=UsaNewonNetflixItem()
        item["netflix_id"]=response.meta["id"]
        item["title"]=response.meta["title"]
        item["show_type"]=response.meta["show_type"]
        item["description"]=response.meta["description"]
        item["year"]=response.meta["year"]
        item["rating"]=response.meta["rating"]
        item["run_time"]=str(response.meta["duration"])
        item["season_number"]=str(response.meta["season_number"])
        item["record_language"]=response.meta["audio"]
        item["url"]=response.meta["url"]
        item["available_season"]=response.meta["available_season"]
        item["image"]=response.meta["image"]
        item["genres"]=response.meta["genres"]
        item["Director"]=response.meta["Director"]
        item["Actor"]=response.meta["Actor"]
        item["subtitles"]=response.meta["subtitles"]
        item["added_to_site"]=response.meta["added_to_site"]
        item["content_type"]=response.meta["content_type"]
        item["history"]=str(response.meta["content_history"])
        item["updated_at"]=datetime.now().strftime('%b %d, %Y')
        print ("\n") 
        print ("Crawling ....",item["updated_at"])
        print (item)
        yield item
