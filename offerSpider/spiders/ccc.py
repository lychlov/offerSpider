# -*- coding: utf-8 -*-
import scrapy


class CccSpider(scrapy.Spider):
    name = 'ccc'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
