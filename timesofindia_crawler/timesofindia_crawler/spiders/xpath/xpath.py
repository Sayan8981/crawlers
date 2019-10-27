import os
import sys


state_url_xpath='//nav[@id="main-nav"]/ul/li[@class="nav-India"]/div[@class="dropdown multi-list"]/ul/li[@data-id="query-%s"]/a/@href'
pagination_xpath='//ul[@class="pagination"]/ul/li[@class="current"]/following-sibling::li/a/@href'
news_headlines_url_xpath='//div/ul/li/span[@class="w_tle"]/a[@hid]/@href'