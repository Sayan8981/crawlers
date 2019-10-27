import os
import sys


state_url_xpath='//nav[@id="main-nav"]/ul/li[@class="nav-India"]/div[@class="dropdown multi-list"]/ul/li[@data-id="query-%s"]/a/@href'
pagination_xpath='//ul[@class="pagination"]/ul/li[@class="current"]/following-sibling::li/a/@href'
news_headlines_url_xpath='//div/ul/li/span[@class="w_tle"]/a[@hid]/@href'


## news_detail_xpath:

news_headlines_xpath='//div[@class="fix_wrap_md clearfix"]/div/div[@class="as_heading"]/h1//text()'
news_headlines_alternative_xpath='//div[@class="clearfix rel"]/div/div/h1//text()'
news_details_xpath='//div[@class="clearfix rel"]/div/div[@class="_3WlLe clearfix  "]//text()'
news_updated_xpath='//div[@class="clearfix rel"]/div/div/div/div/text()'