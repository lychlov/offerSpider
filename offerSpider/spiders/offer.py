# -*- coding: utf-8 -*-
import scrapy


class OfferSpider(scrapy.Spider):
    name = 'offer'
    allowed_domains = ['www.offer.com']
    start_urls = ['http://www.offer.com/']

    def parse(self, response):
        pass
