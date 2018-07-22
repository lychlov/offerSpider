# -*- coding: utf-8 -*-
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import StoreItem, CouponItem
from offerSpider.util import get_header


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
        store_item = StoreItem()
        coupon_item = CouponItem()
        # 处理字段定位

        pass


def get_real_url(url, try_count=1):
    if try_count > 3:
        return url
    try:
        rs = requests.get(url, headers=get_header(), timeout=10)
        if rs.status_code > 400:
            return get_real_url(url, try_count + 1)
        return rs.url
    except:
        return get_real_url(url, try_count + 1)
