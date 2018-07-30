# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class DoubanPipeline(object):

    # def __init__(self, server , port):
    #     self.server = server
    #     self.port = port

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #     s = cls(crawler.settings['MONGODB_SERVER'],
    #             crawler.settings['MONGODB_PORT'])
    #     return s

    def process_item(self, item, spider):
        dict(item)

        return item
