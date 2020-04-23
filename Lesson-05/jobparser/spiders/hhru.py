# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?area=113&st=searchVacancy&text=manager']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[ @class ='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1[@class='bloko-header-1']//text()").extract_first()
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        yield JobparserItem(name=name, salary=salary, link=response.url)