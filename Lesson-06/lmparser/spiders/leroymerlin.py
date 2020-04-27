# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    #start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()

        yield response.follow(next_page, callback=self.parse)

        ads_link = response.xpath("//div[@class='product-name']/a/@href").extract()
        for link in ads_link:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('char_keys', "//dl[@class='def-list']//dt[@class='def-list__term']/text()")
        loader.add_xpath('char_values', "//dl[@class='def-list']//dd[@class='def-list__definition']/text()")
        yield loader.load_item()

        #name = response.xpath("//h1/text()").extract_first()
        #photos = response.xpath("//img[@alt='product image']/@src").extract()
        #yield LmparserItem(name=name, photos=photos)

