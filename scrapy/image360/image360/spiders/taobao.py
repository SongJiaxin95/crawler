# -*- coding: utf-8 -*-
import re
from time import sleep
from urllib.parse import urlencode

import scrapy

from image360.items import GoodsItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com','click.simba.taobao.com','detail.tmall.com']
    params = {}
    def start_requests(self):
        base_url = 'https://s.taobao.com/search?'
        # base_url = 'https://list.tmall.com/search_product.htm?'
        # base_url = 'https://jiangxiaobai.tmall.com/category-1288017932.htm?spm=a1z10.5-b-s.w5001-18218870308.4.38f3789eU7tOlw&search=y&tsearch=y&scene=taobao_shop#TmshopSrchNav'
        for keyword in ['江小白', '五粮液', '泸州老窖']:
            self.params['q'] = keyword
            for page in range(1):
                self.params['s'] = page * 44
                full_url = base_url + urlencode(self.params)
                yield scrapy.Request(url=full_url, callback=self.parse)


    def parse(self, response):
        goods_list = response.css('.item.J_MouserOnverReq')
        for goods in goods_list:
            item = GoodsItem()
            item['deal'] = goods.xpath('div[2]/div[1]/div[2]/text()').extract_first()
            item['price'] = goods.xpath('div[2]/div[1]/div[1]/strong/text()').extract_first()
            title = goods.css('.title a::text').extract()
            title = ''.join(title).strip()
            item['title'] = title
            href = goods.css('.title a::attr("href")').extract_first()
            request = response.follow(href ,callback=self.getImages,dont_filter=True)
            request.meta['item'] = item
            yield request

    def getImages(self, response):
        item = response.meta['item']
        images = response.css('#J_UlThumb li img::attr("src")').extract()
        url_list = []
        for image in images:
            if re.findall(r'https://img',image):
                full_url = re.findall(r'https:.*',image)[0]
            else:
                full_url = 'https:'+image
            url_list.append(full_url)
        item['img_url'] = url_list
        yield item
