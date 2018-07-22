# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from offerSpider.items import StoreItem, CouponItem


class OfferSpider(scrapy.Spider):
    name = 'offer'
    allowed_domains = ['offers.com']
    start_urls = ['https://www.offers.com/stores/']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html)
        letters = soup.find_all('div', class_='letters').find_all('a')
        for letter in letters:
            href = letter.get('href')
            yield scrapy.Request(href, callback=self.letter_page_parse)
        pass

    def letter_page_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html)
        stores = soup.find_all('div', class_='stores-by-letter store-list clearfix pure-g').find_all('a')
        for store in stores:
            href = store.get('href')
            yield scrapy.Request(href, callback=self.store_page_parse)
        pass

    def store_page_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html)
        storeItem = StoreItem()
        couponItem = CouponItem()
        # 处理字段定位

        pass
