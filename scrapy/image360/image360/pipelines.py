# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from pymongo import MongoClient
from redis import Redis
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import logging

from image360.settings import IMAGES_STORE


class SaveImagePipeline(ImagesPipeline):

    logger = logging.getLogger('SaveImagePipeline')

    def get_media_requests(self, item, info):
        for url in item['img_url']:
            print(url)
            yield Request(url=url, meta={'item':item['title']})

    def item_completed(self, results, item, info):
        self.logger.debug('图片下载完成')
        print(results)
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('下载失败')
        item['img_path'] = image_path
        return item

    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split('/')[-1]
        filename = u'{0}/{1}/{2}'.format(info.spider.name, name, image_guid)
        return filename


class SaveToMongoPipeline(object):

    def __init__(self, mongo_url, db_name):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.cilent = None
        self.db = None

    def process_item(self, item, spider):
        self.db[spider.name].insert(dict(item))
        return item

    def open_spider(self, spider):
        self.cilent = MongoClient(self.mongo_url)
        self.db = self.cilent[self.db_name]

    def close_spider(self, spider):
        self.cilent.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGO_URL'),
                   crawler.settings.get('MONGODB_DB'),
                   )

