# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['site'] = 'hh.ru'
            if len(item['salary']) >= 6:
                item['salary_min'] = item['salary'][1].replace('\xa0', '')
                item['salary_max'] = item['salary'][3].replace('\xa0', '')
                item['currency'] = item['salary'][5]
            elif len(item['salary']) < 6:
                if item['salary'][0] == 'от ':
                    item['salary_min'] = item['salary'][1].replace('\xa0', '')
                    item['salary_max'] = float('Nan')
                    item['currency'] = item['salary'][3]
                elif item['salary'][0] == 'до ':
                    item['salary_min'] = float('Nan')
                    item['salary_max'] = item['salary'][1].replace('\xa0', '')
                    item['currency'] = item['salary'][3]
                else:
                    item['salary_min'] = float('Nan')
                    item['salary_max'] = float('Nan')
                    item['currency'] = float('Nan')

        if spider.name == 'sjru':
            item['site'] = 'superjob.ru'
            if len(item['salary']) >= 4:
                item['salary_min'] = item['salary'][0].replace('\xa0', '')
                item['salary_max'] = item['salary'][1].replace('\xa0', '')
                item['currency'] = item['salary'][3]
            elif len(item['salary']) < 4:
                if item['salary'][0] == 'от':
                    item['salary_min'] = item['salary'][2].split('\xa0')[0]+item['salary'][2].split('\xa0')[1]
                    item['salary_max'] = float('Nan')
                    item['currency'] = item['salary'][2].split('\xa0')[2]
                elif item['salary'][0] == 'до':
                    item['salary_min'] = float('Nan')
                    item['salary_max'] = item['salary'][2].split('\xa0')[0] + item['salary'][2].split('\xa0')[1]
                    item['currency'] = item['salary'][2].split('\xa0')[2]
                elif len(item['salary']) == 3:
                    item['salary_min'] = item['salary'][0].replace('\xa0', '')
                    item['salary_max'] = item['salary'][0].replace('\xa0', '')
                    item['currency'] = item['salary'][2]
                else:
                    item['salary_min'] = float('Nan')
                    item['salary_max'] = float('Nan')
                    item['currency'] = float('Nan')


        if item['currency'] == ('руб.'):
            item['currency'] = 'RUB'
        elif item['currency'] == ('EUR'):
             item['currency'] = 'EUR'
        elif item['currency'] == ('USD'):
            item['currency'] = 'USD'
        else:
            item['currency'] = float('Nan')

        item.pop('salary')

        print(item)

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
