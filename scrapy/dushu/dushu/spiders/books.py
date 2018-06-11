# -*- coding: utf-8 -*-
import scrapy
from dushu.items import DushuItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/']
    def parse(self, response):
        li_list = response.xpath('/html/body/div[5]/div/div[2]/div[3]/ul/li')
        for li in li_list:
            item = DushuItem()
            item['name'] = li.xpath('div/h3/a/text()').extract_first()
            item['author'] = li.xpath('div/p[1]/a[1]/text()').extract_first()
            href = li.css('a[href]::attr("href")').re('/book.*')[0]
            url = response.urljoin(href)
            item['url'] = url
            request = scrapy.Request(url=url, callback=self.parse2)
            request.meta['item'] = item
            yield request

    def parse2(self, response):
        item = response.meta['item']
        item['publisher'] = response.xpath('//*[@id="ctl00_c1_bookleft"]/table/tbody/tr[2]/td[2]/a/text()').extract_first()
        item['price'] = response.xpath('//*[@id="ctl00_c1_bookleft"]/p/span/text()').extract_first()
        item['book_describe'] = response.xpath('//*[@class="book-summary"][1]/div/div/text()').extract_first()
        item['author_describe'] = response.xpath('//*[@class="book-summary"][2]/div/div/text()').extract_first()
        item['contents'] = response.xpath('//*[@class="book-summary margin-large-bottom"]/div/div/text()').extract()
        yield item

