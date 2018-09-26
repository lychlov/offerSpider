# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup


class Saveon2Spider(scrapy.Spider):
    name = 'saveon2'
    allowed_domains = ['saveoncannabis.com']
    start_urls = ['https://www.saveoncannabis.com/coupons/']
    page_urls = 'https://www.saveoncannabis.com/coupons/2/'

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        if not re.findall(r'/coupons/(.+?)/', response.url):
            max_page = int(soup.find('ul', class_='page-numbers').find('a').text)
            for i in range(2, max_page + 1):
                yield scrapy.Request(url=self.page_url % i, callback=self.parse)

        pass
