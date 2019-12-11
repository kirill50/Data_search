# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy252

    def employerHH(self,item):
        employer=''
        item['employer'] = employer.join(item['employer']).replace('\xa0', ' ')
        return item['employer']

    def process_item(self, item, spider):
        #print(item)
        if spider.name == 'hhru':
            item['employer']=self.employerHH(item)

            if not item['min_salary']:
                item['min_salary']= None
            else:
                item['min_salary']=item['min_salary'][0]

            if not item['max_salary']:
                item['max_salary']= None
            else:
                item['max_salary']=item['max_salary'][0]

            if not item['currency']:
                item['currency'] = None
            else:
                item['currency'] = item['currency'][0]

        elif spider.name == 'sjru':
            if not item['min_salary']:
                item['min_salary']=None
            else:
                item['min_salary']=item['min_salary'].replace('\xa0', ' ')

            if not item['max_salary']:
                item['max_salary']=None
            else:
                item['max_salary']=item['max_salary'].replace('\xa0', ' ')

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        print(item)
        return item

