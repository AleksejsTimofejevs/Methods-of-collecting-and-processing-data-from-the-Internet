# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from urllib.parse import urlparse
import scrapy
import os
import re

class LmparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lm_photo
    def process_item(self, item, spider):
        item['characteristics'] = dict(zip(item['char_keys'], item['char_values']))
        del item['char_keys']
        del item['char_values']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        folder = re.findall(r'\d+', os.path.basename(urlparse(request.url).path))[0] + '/'
        return f'full/{folder}' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
