import scrapy
from scrapy import *
import os
import sys
#import pdb;pdb.set_trace()
print(sys.path)
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class hindunews(Spider):
    
    name="hindunews"
    start_urls=['https://www.thehindu.com/']

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
            if 'national' in urls:
                yield Request(url=urls,callback=self.parse_national_news_url,dont_filter=True)
            elif 'international' in urls:
                yield Request(url=urls,callback=self.parse_international_news_url,dont_filter=True)    
            elif 'state' in urls:
                yield Request(url=urls,callback=self.parse_states_news_url,dont_filter=True)
            elif 'cities' in urls:
                yield Request(url=urls,callback=self.parse_cities_news_url,dont_filter=True)
            elif 'multimedia' in urls:
                yield Request(url=urls,callback=self.parse_multimedia_news_url,dont_filter=True)
            elif 'entertainment' in urls:
                yield Request(url=urls,callback=self.parse_entertainment_news_url,dont_filter=True)
            elif 'sport' in urls:
                yield Request(url=urls,callback=self.parse_sports_news_url,dont_filter=True)
            elif 'business' in urls :
                yield Request(url=urls,callback=self.parse_business_news_url,dont_filter=True)
            elif 'science' in urls:
                yield Request(url=urls,callback=self.parse_science_news_url,dont_filter=True)
            elif 'health' in urls:
                yield Request(url=urls,callback=self.parse_health_news_url,dont_filter=True)
            elif 'technology' in urls:
                yield Request(url=urls,callback=self.parse_technology_news_url,dont_filter=True)
            elif 'education' in urls:
                yield Request(url=urls,callback=self.parse_education_news_url,dont_filter=True)
            else:
                print ("The url is not valid",urls) 

    def national_news_pagination(self,selector):
        import pdb;pdb.set_trace()
        national_news_nextpage_url=selector.xpath('//div/ul[@class="pagination"]/li[@class="next page-item"]/a/@href').extract()
        if national_news_nextpage_url:
            yield Request(national_news_nextpage_url[0],callback=self.parse_national_news_url,dont_filter=True)

    def parse_national_news_url(self,national_news_page_url):
        import pdb;pdb.set_trace()
        yield Request(national_news_page_url.url,callback=self.national_news_headlines_url)
        sel=Selector(national_news_page_url)
        self.national_news_pagination(sel)

    def national_news_headlines_url(self,national_news_page_url):
        import pdb;pdb.set_trace()
        print(national_news_page_url.url)    

    def parse_international_news_url(self,international_news_url):
        pass

    def parse_entertainment_news_url(self,entertainment_news_url):
        pass    
    def parse_states_news_url(self,states_news_url):
        pass
    def parse_cities_news_url(self,cities_news_url):
        pass 
    def parse_multimedia_news_url(self,multimedia_news_url):
        pass 
    def parse_sports_news_url(self,sports_news_url):
        pass 
    def parse_business_news_url(self,business_news_url):
        pass 
    def parse_science_news_url(self,science_news_url):
        pass
    def parse_health_news_url(self,health_news_url):
        pass
    def parse_technology_news_url(self,technology_news_url):
        pass
    def parse_education_news_url(self,education_news_url):
        pass


                
                          
                    
                
                
                    
                    
        