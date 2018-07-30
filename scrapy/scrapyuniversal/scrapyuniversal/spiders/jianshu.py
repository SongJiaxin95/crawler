# -*- coding: utf-8 -*-
from ast import literal_eval

import requests
import scrapy


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    # start_urls = ['https://www.jianshu.com/u/d84fda68a2c0']

    def start_requests(self):
        yield scrapy.Request('https://www.jianshu.com/u/d84fda68a2c0', callback=self.parse)

    def parse(self, response):
        li_list = response.css('.note-list li')
        for elem in li_list:
            href = elem.css('.title::attr("href")').extract_first()
            href = response.urljoin(href)
            print(href)
            # resp = requests.get(href)
            for i in range(50):
                proxy = literal_eval(requests.get('http://localhost:5000/'))
                print(proxy)
                requests.get(url=href,proxies=proxy)

    # def content(self, response):
    #     title = response.css('h1').extract_first()
    #     print(title)


