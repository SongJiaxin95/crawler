# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import pymongo
from scrapy import log
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):

    connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    db = connection[settings['MONGODB_DB']]
    collection = db[settings['MONGODB_COLLECTION']]

    # def process_item(self, item, spider):
    #     valid = True
    #     for data in item:
    #         if not data:
    #             valid = False
    #             raise DropItem("Missing %s of blogpost from %s" % (data, item['url']))
    #     if valid:
    #         self.collection.insert(dict(item))
    #         log.msg("Item wrote to MongoDB database %s/%s" %
    #                 (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
    #                 level=log.DEBUG, spider=spider)
    #     return item
        # pass
    def get_media_requests(self, item, info):
        # for image_url in item['img_url']:
        yield Request(item['img_url'], meta={'item': item['img_name']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(name, image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path[0]
        self.collection.insert(dict(item))
        return item


