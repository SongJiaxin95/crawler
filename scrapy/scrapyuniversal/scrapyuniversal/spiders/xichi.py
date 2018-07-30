# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapyuniversal.items import ScrapyuniversalItem


class XichiSpider(CrawlSpider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    # start_urls = ['http://www.xicidaili.com/nn/']

    def start_requests(self):
        base_url = 'http://www.xicidaili.com/nn/'
        for page in range(50):
            full_url = os.path.join(base_url, str(page + 1))
            yield scrapy.Request(url=full_url, callback=self.parse_item)

    # rules = (
    #     Rule(LinkExtractor(allow=r'http://www.xicidaili.com/nn/\d*'), callback='parse_item')
    # )

    def parse_item(self, response):
        item = ScrapyuniversalItem()
        for proxy in response.css('#ip_list tr'):
            item['host'] = proxy.xpath('td[2]/text()').extract_first()
            item['port'] = proxy.xpath('td[3]/text()').extract_first()
            item['type'] = proxy.xpath('td[6]/text()').extract_first()
            yield item
