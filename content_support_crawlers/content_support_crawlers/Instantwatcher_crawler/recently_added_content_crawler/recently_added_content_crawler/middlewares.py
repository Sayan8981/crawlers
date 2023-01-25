# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
import base64
import random
from scrapy import signals
from w3lib.http import basic_auth_header
from twisted.internet.error import *
import base64
proxy_list = ['us-atl.secureconnect.me','us-la.secureconnect.me','us-fl.secureconnect.me','us-dal.secureconnect.me','us-nj.secureconnect.me','us-ny.secureconnect.me','us-chi.secureconnect.me','us-sf.secureconnect.me','us-sa.secureconnect.me','us-slc.secureconnect.me',]

class RecentContentCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        
        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RecentlyAddedContentCrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        #request.meta['proxy'] = "https://134.122.17.137:8080"
        #proxy_user_pass = "vinuthna@headrun.com:Hotthdrn591!@"
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = 'http://'+ proxy+':6060'
        request.headers['Proxy-Authorization'] = basic_auth_header('vinuthna@headrun.com','Hotthdrn591!')
        # Use the following lines if your proxy requires authentication
        #return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        return None
        
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)