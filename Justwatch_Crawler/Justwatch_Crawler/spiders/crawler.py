import scrapy 
from scrapy import *
import sys
import os
import time,json,logging,requests
requests = requests.Session()
import pinyin,unidecode
from scrapy import signals
from datetime import datetime,timedelta
from Justwatch_Crawler.items import *
sys.path.insert(0,os.getcwd()+"/xpath")
sys.path.insert(1,os.getcwd()+"/operation")
# import create_db_tables
# import db_output
# from db_output import db_output_stats
# from send_mail import send_emails


class justwatchbrowse(Spider):

    name="justwatchbrowse"
    start_urls=[]
    allowed_domain=["https://apis.justwatch.com/"]
    
    #TODO: Requested API urls noted here
    def request_urls(self):
        self.providers_url=self.allowed_domain[0]+"content/providers/locale/en_US"
        self.api_url=str(self.allowed_domain[0])+'content/titles/en_US/new?body={"age_certifications":[],"content_types":["%s"],"genres":[],"languages":null,"min_price":null,"matching_offers_only":null,"max_price":null,"monetization_types":[],"presentation_types":[],"providers":["%s"],"release_year_from":%d,"release_year_until":null,"scoring_filter_types":null,"page":0,"page_size":1000}'
        self.movies_meta_url=self.allowed_domain[0]+"content/titles/movie/%s/locale/en_US"
        self.series_meta_url=self.allowed_domain[0]+"content/titles/show/%s/locale/en_US"
        self.season_meta_url=self.allowed_domain[0]+"content/titles/show_season/%s/locale/en_US"

    #initialization:
    def __init__(self):
        self.request_urls()
        self.provider_response=""
        self.provider_details=[]
        self.providers_list=[]
                    
    def start_requests(self):
        #import pdb;pdb.set_trace()
        url = self.providers_url
        yield FormRequest(str(url), callback = self.provider_browse, dont_filter=True)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(justwatchbrowse, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    #TODO: to get the signal when spider closing
    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s" % spider.name)
        # Whatever is here will run when the spider is done.
        # print ("Preparing to create csv file from database...............")
        # db_output_stats().main()
        # time.sleep(10)
        # print("Preparing to send email to client.................")
        # send_emails().main()

    def cleanup(self):
        pass

    #TODO: TO take the provider details
    def provider_browse(self,response):
        #import pdb;pdb.set_trace()
        self.provider_response=json.loads(response.body.decode())
        for data in self.provider_response:
            if data["technical_name"]=="hulu" or data["technical_name"]=="hbogo" or data["technical_name"]=="showtime":
                self.provider_details.append({"provider_id":data["id"],"service_name":data["clear_name"],"provider":data["short_name"]})
        logging.info({"providers_details":self.provider_details})        
        yield FormRequest(str(response.url),callback=self.parse_providers,meta={"providers":self.provider_details},dont_filter= True) 
   
    #TODO: parsing the providers of movies and shows to get Data
    def parse_providers(self,response):
        logging.info (response.meta)
        yield FormRequest(url=response.url,callback=self.justwatch_movie_browse,meta=response.meta,dont_filter=True)
        yield FormRequest(url=response.url,callback=self.justwatch_tvshow_browse,meta=response.meta,dont_filter=True)

    #TODO: Browse the Movie response
    def justwatch_movie_browse(self,response):    
        self.providers_list=response.meta["providers"]
        for data in self.providers_list:
            provider=data["provider"]
            movie_url=self.api_url%("movie",str(provider),eval(datetime.now().strftime("%Y")))
            resp=requests.request("GET",movie_url, data={},headers={})
            if resp.status_code == 200:
                #import pdb;pdb.set_trace()
                movie_response=json.loads(resp.text)
                yield FormRequest(url=str(movie_url),callback=self.justwatch_movies_terminal,meta={"provider":data["provider"],"provider_id":data["provider_id"],"service_name":data["service_name"],'data':movie_response},dont_filter=True)
            else:
                logging.info("movie_response status", resp.status_code)    

    #TODO: Browse the Tvshow response
    def justwatch_tvshow_browse(self,response):  
        self.providers_list=response.meta["providers"]
        for data in self.providers_list:
            provider=data["provider"]  
            show_url=self.api_url%("show",str(provider),eval(datetime.now().strftime("%Y")))
            resp=requests.request("GET",show_url, data={},headers={})
            if resp.status_code == 200:
                #import pdb;pdb.set_trace()
                show_response=json.loads(resp.text)
                yield FormRequest(url=str(show_url),callback=self.justwatch_tvshow_terminal,meta={"provider":data["provider"],"provider_id":data["provider_id"],"service_name":data["service_name"],'data':show_response},dont_filter=True)
            else:
                logging.info("Tvshow_response status", resp.status_code)  

    def justwatch_movies_terminal(self,response):            
        logging.info(response.meta) 

    def justwatch_tvshow_terminal(self,response):
        logging.info(response.meta)     