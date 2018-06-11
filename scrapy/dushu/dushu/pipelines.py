# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class DushuPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing %s of blogpost from %s" % (data, item['url']))
        if valid:
            # new_book = [{
            #     'name':item['name'],
            #     'author':item['author'],
            #     'url':item['url'],
            #     'book_describe':item['book_describe'],
            #     'author_describe':item['author_describe'],
            #     'publisher':item['publisher'],
            #     'price':item['price'],
            #     'contents':item['contents'],
            # }]
            self.collection.insert(dict(item))
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        return item
