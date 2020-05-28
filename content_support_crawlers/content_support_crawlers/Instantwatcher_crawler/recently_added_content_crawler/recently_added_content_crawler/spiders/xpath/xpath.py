source_node='//span[@class="site-switch"]/a/text()'

source_url_xpath='//span/a[contains(text(),"%s")]/@href'

section_xpath='//span[@class="provider"][contains(text(),"%s")]/following-sibling::a/text()'

section_urls='//span[@class="provider"][contains(text(),"%s")]/following-sibling::a/@href'

checked_content_type_xpath='//li[@class="filter-item filter-active"]/label/span[@class="filter-item-link"]/text()'

checked_content_type_key_xpath='//label[span[contains(text(),"%s")]]/input/@value'

next_page='//div/ul/li/following-sibling::li/a[@class="next-page"]/@href'

title_xpath='//*[preceding-sibling::h4[contains(text(),"%s")]]/span[@class="title"]/a/text()'

year_xpath='//*[preceding-sibling::h4[contains(text(),"%s")]][span[@class="title"]/a[contains(text(),"%s")]]/span[@class="year"]/text()'