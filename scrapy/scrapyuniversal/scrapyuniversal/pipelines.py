# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy.exceptions import DropItem
import json

class ScrapyuniversalPipeline(object):

    def __init__(self, host, port, password):
        self.client = redis.Redis(host=host, port=port, password=password)
        self.client.flushall()

    def process_item(self, item, spider):
        vaild = True
        for data in item:
            if not data:
                vaild = False
                raise DropItem("Missing %s of blogpost from %s" % (data, item['url']))
        if vaild:
            proxy = json.dumps(dict(item))
            self.client.rpush('proxy', proxy)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('REDIS_HOST'),
                   crawler.settings.get('REDIS_PORT'),
                   crawler.settings.get('REDIS_PASSWORD'),
                   )
