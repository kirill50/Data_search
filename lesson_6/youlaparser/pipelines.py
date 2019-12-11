# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class DataBasePipeline(object):
    def __init__(self):
        client=MongoClient('localhost', 27017)
        self.mongo_base=client.youla_photo

    def process_item(self, item, spider):
        # if not item['price']:
        #     item['price'] = None
        # else:
        #     item['price']=int(item['price'].replace('\u2009', ''))

        collection=self.mongo_base[spider.name]
        collection.update_one(item,{'$set':item},upsert=True)
        return item

class YoulaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    # img=img.replace('background-image:url(','')
                    # img=img.replace(')','')
                    # img=img.replace('/s/','/l/')
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        pass
