# -*- coding: utf-8 -*-
import re

import scrapy
from geyan.items import GeyanItem


class SentenceSpider(scrapy.Spider):
    name = 'sentence'
    allowed_domains = ['www.geyanw.com']
    start_urls = ['https://www.geyanw.com/']

    def parse(self, response):
        dl_list = response.xpath('//*[@id="p_left"]/div/dl')
        for elem in dl_list:
            item = GeyanItem()
            item['title'] = elem.xpath('dt/strong/a/text()').extract_first()
            hrefs = dl_list[0].xpath('dd/ul/li/a/@href').extract()
            contents = []
            for href in hrefs:
                url = response.urljoin(href)
                content = {'url':url}
                request = response.follow(url=url,callback=self.sentence)
                request.meta['content'] = content
                yield request
                contents.append(content)
            item['content'] = contents
            yield item



    def sentence(self, response):
        content = response.meta['content']
        content['second_title'] = response.xpath('//*[@id="p_left"]/div[1]/div[2]/h2/text()').extract_first()
        my_list = []
        sentences = response.xpath('//*[@id="p_left"]/div[1]/div[4]/p/text()').extract()
        for sentence in sentences:
            if re.match(r'\b.*',sentence):
                my_list.append(sentence)
        content['sentence'] = my_list
        return content

