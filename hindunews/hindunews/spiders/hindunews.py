import scrapy

class hindunews(scrapy.Spider):
    
    name="hindunews"
    start_urls=['https://www.thehindu.com/']

    def parse(self,response):
        #import pdb;pdb.set_trace()
        #print (response.body)
        sel=scrapy.Selector(response)
        url=sel.xpath('//div[@class="col-xs-12"]/nav/div[@id="main-menu"]/ul/li[@class="dropdown"]/a/@href').extract()
        print(url)
        for url in url:
        	if "news" in url:
        		news_url=url
        yield scrapy.Request(news_url, callback=self.parse_url,dont_filter=True)

    def parse_url(self,news_url):
        print (news_url.url)
        print (news_url.body)    