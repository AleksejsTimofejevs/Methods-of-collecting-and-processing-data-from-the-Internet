# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import TakeFirst, MapCompose

def cleaner_value(value):
    value = re.findall(r'\S+', value)
    value = ' '.join(value)
    return value

class LmparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    char_keys = scrapy.Field()
    char_values = scrapy.Field(input_processor=MapCompose(cleaner_value))
    characteristics = scrapy.Field()

    #input_processor=MapCompose(cleaner_value)
