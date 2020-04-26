# -*- coding: utf-8 -*-

# Scrapy settings for Justwatch_Crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os,logging
from twisted.internet import defer, protocol, reactor # the reactor

PROJECT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

BOT_NAME = 'Justwatch_Crawler'

SPIDER_MODULES = ['Justwatch_Crawler.spiders']
NEWSPIDER_MODULE = 'Justwatch_Crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Linux; Veveobot; + http://corporate.veveo.net/contact/) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0" 
#'Justwatch_Crawler (+http://www.yourdomain.com)'
LOG_FILE = None #-> for every run, a log willl be saved as of a phone logs
LOG_LEVEL = 'INFO' #'DEBUG'

DOWNLOAD_DELAY = 0.5 #- > time betwwn the request and response
DOWNLOAD_TIMEOUT = 360 #-> if we dont get response from site with in 360 secs, the rquest will get timedout
RANDOMIZE_DOWNLOAD_DELAY = True
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'Accept-Encoding': '*'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'Justwatch_Crawler.middlewares.JustwatchCrawlerSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Justwatch_Crawler.middlewares.JustwatchCrawlerDownloaderMiddleware': 543,
}

RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Justwatch_Crawler.pipelines.JustwatchCrawlerPipeline': 300,
}
LOG_ENABLED = True

LOG_FILE= 'script.log'
LOG_LEVEL= 'INFO'
      
if PROJECT_DIR+'/spiders/'+LOG_FILE:
	os.remove(PROJECT_DIR+'/spiders/'+LOG_FILE)
logging.getLogger().addHandler(logging.StreamHandler())

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
TELNETCONSOLE_ENABLED=False
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
