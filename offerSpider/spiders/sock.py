# -*- coding: utf-8 -*-
import scrapy


class SockSpider(scrapy.Spider):
    name = 'sock'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
