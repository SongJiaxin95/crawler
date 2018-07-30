# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import scrapy
from json import loads
from image360.items import BeautyItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/']

    def start_requests(self):
        base_url = 'https://image.so.com/zj?'
        param = {'ch': 'beauty', 'listtype': 'new', 'temp':1}
        for page in range(50):
            param['sn'] = page * 30
            full_url = base_url + urlencode(param)
            yield scrapy.Request(url=full_url, callback=self.parse)


    def parse(self, response):
        model_dict = loads(response.text)
        for elem in model_dict['list']:
            item = BeautyItem()
            item['title'] = elem['group_title']
            item['tag'] = elem['tag']
            item['width'] = elem['cover_width']
            item['height'] = elem['cover_height']
            item['img_url'] = [elem['qhimg_url']]
            yield item
