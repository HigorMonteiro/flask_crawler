# -*- coding: utf-8 -*-
import scrapy


class HalcaSpider(scrapy.Spider):
    name = 'halca'
    allowed_domains = ['https://halcaimobiliaria.com.br/alugar']
    start_urls = ['http://https://halcaimobiliaria.com.br/alugar/']

    def parse(self, response):
        pass
