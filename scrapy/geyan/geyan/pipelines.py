# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from geyan import settings
class GeyanPipeline(object):
    cilent = pymongo.MongoClient(host=settings.MONGODB_SERVER,port=settings.MONGODB_PORT)
    def process_item(self, item, spider):
        # self.cilent[settings.MONGODB_DB][settings.MONGODB_COLLECTION].insert(dict(item))
        print(item)
        return item

