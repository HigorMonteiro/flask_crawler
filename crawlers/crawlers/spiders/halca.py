# -*- coding: utf-8 -*-
import scrapy
from pip._vendor.urllib3 import response
from urllib.parse import urljoin

class HalcaSpider(scrapy.Spider):

    name = 'halca'
    allowed_domains = ['halcaimobiliaria.com.br']
    start_urls = ['http://halcaimobiliaria.com.br/alugar',]

    def parse(self, response):
        items = response.xpath('//div[contains(@class, "bloco-imovel")]')
        for item in items:
            urls = []
            urls.append(item.xpath('./a/@href').extract_first())
            for i in urls:
                yield scrapy.Request(
                    urljoin('http://halcaimobiliaria.com.br/',
                            i[1:]),callback=self.parse_detail
                )
        next_page = response.xpath(
            '/html/body/section/div[2]/div[5]/div/nav/ul/li[15]/a/@href'
        )
        if next_page:
            self.log('Próxima página: {}'.format(next_page.extract_first()))
            yield scrapy.Request(
                urljoin('http://halcaimobiliaria.com.br/alugar',
                        next_page.extract_first()),callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath(
            """//h1[contains(@class, "titulo")]//text()"""
        ).extract_first()
        address = response.xpath(
            """//div[contains(@class, "bloco")]
            /div[contains(@class, "resumo")]/p//text()"""
        ).extract_first()
        value = response.xpath(
            """//div[contains(@class, "bloco")]
            /div[contains(@class, "valor")]//text()"""
        ).extract_first()
        characteristics = response.xpath(
            """
            //div[contains(@class, "caracteristicas")]/p//text()"""
        ).extract_first()
        yield {
            'category': 'Aluguel',
            'title': title,
            'address': address,
            'value': value.strip('\n R$ \n'),
            'characteristics': characteristics,
        }
