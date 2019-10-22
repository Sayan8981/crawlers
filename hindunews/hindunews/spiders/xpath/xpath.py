import sys


url_xpath='//div[@class="col-xs-12"]/nav/div[@id="main-menu"]/ul/li[@class="dropdown"]/a/@href'
different_news_xpath='//section/section/div[@class="container section-header "]/div/h2[@class="section-heading left"]/a/@href'
news_pagination_xpath='//div/ul[@class="pagination"]/li[@class="next page-item"]/a/@href'

#national_news_xpath
national_storycard_new_xpath='//div/div[@class="story-card"]/a/@href'
national_otherstorycard_news_xpath='//div/div/div[@class="Other-StoryCard"]/a/@href'
national_news_headlines_xpath='//div[@class=" "]/h1//text()'
national_news_tagline_xpath='//div[@class=" "]/h2//text()'
national_news_details_xpath='//div[@class=" "]/div[@id]/p//text()'
national_news_details_altnernative_xpath='//div[@class=" "]/div/div[@id]/p//text()'
national_news_country_xpath='//div[@class=" "]/div/div[@class="ut-container"]/span//text()'
national_news_date_xpath='//div[@class=" "]/div/div[@class="ut-container"]/span/none//text()'
national_news_updatedDate_xpath='//div[@class=" "]/div/div[@class="ut-container"]/div/span/none//text()'