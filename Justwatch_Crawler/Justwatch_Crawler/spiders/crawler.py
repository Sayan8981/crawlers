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

# TO crawl the keep-up content from Justwwatch (Hulu,Showtime,HBOGO)

class justwatchbrowse(Spider):

    name="justwatchbrowse"
    start_urls=[]
    allowed_domain=["https://apis.justwatch.com/"]
    sources_list=["hulu","hbogo","showtime"]
    
    #TODO: Requested API urls noted here
    def request_urls(self):
        self.providers_url=self.allowed_domain[0]+"content/providers/locale/en_US"
        self.api_url=str(self.allowed_domain[0])+'content/titles/en_US/new?body={"age_certifications":[],"content_types":["%s"],"genres":[],"languages":null,"min_price":null,"matching_offers_only":null,"max_price":null,"monetization_types":[],"presentation_types":[],"providers":["%s"],"release_year_from":%d,"release_year_until":null,"scoring_filter_types":null,"page":0,"page_size":1000}'
        self.movies_meta_url=self.allowed_domain[0]+"content/titles/movie/%s/locale/en_US"
        self.series_meta_url=self.allowed_domain[0]+"content/titles/show/%s/locale/en_US"
        self.season_meta_url=self.allowed_domain[0]+"content/titles/show_season/%s/locale/en_US"
        self.genres_api=self.allowed_domain[0]+"content/genres/locale/en_US"

    #initialization:
    def __init__(self):
        self.request_urls()
        self.provider_response=""
        self.provider_details=[]
        self.providers_list=[]
        self.date=''
        self.item_id=0
        self.movies_meta=dict()
        self.video_info_dict=dict()
        self.video_info=[]
        self.credits_info=[]
        self.credits_dict=dict()
        self.genres_info=[]
        self.rating_info=[]
                    
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
        self.movies_meta=dict()
        self.video_info=[]
        self.credits_info=[]
        self.genres_info=[]
        self.rating_info=[]

    def fetch_response_for_api(self,api):
        response=requests.request("GET",api, data={},headers={})
        return response   

    #TODO: TO take the provider details
    def provider_browse(self,response):
        self.provider_response=json.loads(response.body.decode())
        for data in self.provider_response:
            if data["technical_name"] in self.sources_list:
                self.provider_details.append({"provider_id":data["id"],"service_name":data["clear_name"],"provider":data["short_name"]})
        logging.info({"providers_details":self.provider_details})        
        yield FormRequest(str(response.url),callback=self.parse_providers,meta={"providers":self.provider_details},dont_filter= True) 
   
    #TODO: parsing the providers of movies and shows browse to get Data
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
            resp=self.fetch_response_for_api(movie_url)
            if resp.status_code == 200:
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
            resp=self.fetch_response_for_api(show_url)
            if resp.status_code == 200:
                show_response=json.loads(resp.text)
                yield FormRequest(url=str(show_url),callback=self.justwatch_tvshow_terminal,meta={"provider":data["provider"],"provider_id":data["provider_id"],"service_name":data["service_name"],'data':show_response},dont_filter=True)
            else:
                logging.info("Tvshow_response status", resp.status_code)  

    #TODO: Browse to get only movie_sk and date 
    def justwatch_movies_terminal(self,response):            
        try:
            movie_data=response.meta["data"]["days"]
            if movie_data:
                for data in movie_data:
                    self.date=data["date"]
                    self.item_id=data["providers"][0]["items"][0]["id"]
                    yield FormRequest(url=response.url,callback=self.justwatch_movies_meta,meta={"provider_details":response.meta,"date":self.date,"movie_sk":self.item_id,},dont_filter=True)
            else:
                logging.info("No movies are available today .................")        
        except Exception as error:
            logging.info("Exception caught .......", error, type(error),response.url)                

    #TODO: to get OTT related info
    def get_ott_link_info(self,ott_info):
        if ott_info:
            for info in ott_info:
                self.video_info_dict=dict()
                self.video_info_dict["urls"]=info["urls"]
                self.video_info_dict["quality"]=info["presentation_type"]
                self.video_info_dict["currency"]=info["currency"]
                try:
                    self.video_info_dict["price"]=info["retail_price"]
                    self.video_info_dict["purchase_type"]=info["monetization_type"]
                except KeyError:
                    pass
                self.video_info.append(self.video_info_dict)
            return self.video_info
        else:
            return self.video_info        

    #TODO: To get credits related info  
    def get_credits_info(self,credits_info):
        if credits_info:
            for info in credits_info:
                self.credits_dict=dict()
                self.credits_dict["role"]=info["role"]
                self.credits_dict["name"]=unidecode.unidecode(pinyin.get(info["name"]))
                self.credits_info.append(self.credits_dict)
            return self.credits_info
        else:
            return self.credits_info   

    #TODO: To get genres related info 
    def get_genres_info(self,genre_ids):
        if genre_ids:
            genres_response=self.fetch_response_for_api(self.genres_api)
            if genres_response.status_code==200:
                for ids in genre_ids:
                    for data in json.loads(genres_response.text):
                        if data["id"]==ids:
                            self.genres_info.append(data["translation"])
                return "{}".format(self.genres_info)
            else:
                return self.genres_info     
        else:
            return self.genres_info

    def get_rating_info(self,rating_info):
        #import pdb;pdb.set_trace()
        if rating_info:
            for info in rating_info:
                if "meter" in info["provider_type"] or "score" in info["provider_type"]:
                    self.rating_info.append(info)    
            return self.rating_info
        else:
            return self.rating_info               

    #TODO: TO get movies meta data  
    def get_movies_info(self,movie_url):
        movie_response=self.fetch_response_for_api(movie_url)
        if movie_response.status_code==200:
            movie_response = json.loads(movie_response.text)
            self.movies_meta["movie_id"] = movie_response["id"]   
            self.movies_meta["title"] = unidecode.unidecode(pinyin.get(movie_response["title"]))
            self.movies_meta["description"] = unidecode.unidecode(pinyin.get(movie_response["short_description"]))
            self.movies_meta["release_year"] = movie_response["original_release_year"]
            try:
                self.movies_meta["original_title"] = unidecode.unidecode(pinyin.get(movie_response["original_title"]))
            except KeyError:
                self.movies_meta["original_title"]=""    
            try:    
                self.movies_meta["ott"] = self.get_ott_link_info(movie_response["offers"])
            except KeyError:
                self.movies_meta["ott"] = []
            try:        
                self.movies_meta["credits"] = self.get_credits_info(movie_response["credits"])  
            except KeyError:
                self.movies_meta["credits"] = "Null"
            try:                         
                self.movies_meta["duration"] = "{} {}".format(str(movie_response["runtime"]),"mins")
            except KeyError:
                self.movies_meta["duration"] = "Null" 
            try:       
                self.movies_meta["genres"] = self.get_genres_info(movie_response["genre_ids"])
            except KeyError:
                self.movies_meta["genres"] = "Null"  
            try:
                self.movies_meta["age_rating"] = movie_response["age_certification"]
            except KeyError:
                self.movies_meta["age_rating"] = "Null"  
            try:
                self.movies_meta["rating"] = self.get_rating_info(movie_response["scoring"])
            except KeyError:
                self.movies_meta["rating"] = "Null"              
            return self.movies_meta
        else:
            return self.movies_meta     

    #TODO: Browse the metadata fo movies 
    def justwatch_movies_meta(self,response): 
        self.cleanup()  
        movies_sk=response.meta["movie_sk"]
        movie_meta_url=self.movies_meta_url%movies_sk
        movie_meta_info=self.get_movies_info(movie_meta_url)
        if movie_meta_info!={}:
            yield FormRequest(url=str(movie_meta_url),callback=self.movies_item_stored,meta={"provider_details":response.meta,"data":movie_meta_info},dont_filter=True)

    def justwatch_tvshow_terminal(self,response):
        pass 

    #TODO: storing required field though items file 
    def movies_item_stored(self,response):
        item=MovieItem()
        item["movie_id"] = response.meta["data"]["movie_id"]
        item["title"] = response.meta["data"]["title"]
        item["original_title"] = response.meta["data"]["original_title"]
        item["description"] = response.meta["data"]["description"]
        item["release_year"] = response.meta["data"]["release_year"]
        item["ott"] = response.meta["data"]["ott"]
        item["credits"] = response.meta["data"]["credits"]
        item["rating"] = response.meta["data"]["rating"]
        item["duration"] = response.meta["data"]["duration"]
        item["genres"] = response.meta["data"]["genres"] 
        item["age_rating"] = response.meta["data"]["age_rating"]
        item["provider_id"] = response.meta["provider_details"]["provider_details"]["provider_id"]
        item["service_name"] = response.meta["provider_details"]["provider_details"]["service_name"]
        item["added_to_site"] = response.meta["provider_details"]["date"]
        item["updated_at"] = datetime.now().strftime("%d-%m-%Y")
        logging.info("\n")
        logging.info(item)
        yield item