# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import CouponItem, StoreItem


class VapingSpider(scrapy.Spider):
    name = 'vaping'
    allowed_domains = ['vaping.coupons/']
    start_urls = ['https://vaping.coupons/stores/']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        stores_list = soup.find_all('ul', class_='stores')
        for stores in stores_list:
            for store in stores.find_all('a'):
                store_link = store.get('href')
                total = re.findall(r'\((.+?)\)', str(store))[0]
                if total != 0:
                    for i in range(int(int(total) / 10) + 1):
                        yield scrapy.Request(url=store_link + 'page/%s/' % (i + 1), callback=self.coupon_parse)

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find_all('div', class_='type-coupon')
        for coupon_info in coupon_infos:
            coupon = CouponItem()
            coupon['type'] = 'coupon'
            coupon['name'] = ''
            coupon['site'] = ''
            coupon['description'] = ''
            coupon['verify'] = ''
            coupon['link'] = ''
            coupon['expire_at'] = ''
            coupon['coupon_type'] = ''
            coupon['code'] = ''
            coupon['final_website'] = ''
            coupon['store'] = ''
            coupon['store_url_name'] = ''
            coupon['store_description'] = ''
            coupon['store_category'] = ''
            coupon['store_website'] = ''
            coupon['store_country'] = ''
            coupon['store_picture'] = ''
            coupon['created_at'] = ''
            coupon['status'] = ''
            coupon['depth'] = ''
            coupon['download_timeout'] = ''
            coupon['download_slot'] = ''
            coupon['download_latency'] = ''
        pass
