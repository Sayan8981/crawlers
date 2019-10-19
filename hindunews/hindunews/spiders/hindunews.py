import scrapy

class hindunews(scrapy.Spider):
    
    name="hindunews"
    start_urls=['https://www.thehindu.com/']

    def parse(self,response):
        #import pdb;pdb.set_trace()
        print (response.body)