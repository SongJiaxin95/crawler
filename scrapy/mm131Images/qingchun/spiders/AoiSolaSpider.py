# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from qingchun.items import QingchunItem

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['www.mm131.com']
    start_urls = [
        # 'http://www.mm131.com/xinggan/',
        'http://www.mm131.com/qingchun/',
        # 'http://www.mm131.com/xiaohua/',
        # 'http://www.mm131.com/chemo/',
        # 'http://www.mm131.com/qipao/',
        # 'http://www.mm131.com/mingxing/'
        ]

    def parse(self, response):
        image_list = response.css(".list-left dd:not(.page)")
        for img in image_list:
            img_name = img.css('a::text').extract_first()
            img_url = str(img.css('a::attr("href")').extract_first())
            print(img_url)
            next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_first()
            if next_url is not None:
                yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(img_url, callback=self.content)


    def content(self, response):
        item = QingchunItem()
        item['img_name'] = response.css('.content h5::text').extract_first()
        image_url = response.css(".content-pic img::attr('src')").extract()
        item['img_url'] = image_url[0]
        yield item
        next_url = response.css(".page-ch:last-child::attr(href)").extract_first()
        if next_url is not None:
            yield response.follow(next_url, callback=self.content)

