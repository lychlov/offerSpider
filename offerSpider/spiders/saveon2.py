# -*- coding: utf-8 -*-
import datetime
import re

import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import CouponItem
from offerSpider.util import get_header


class Saveon2Spider(scrapy.Spider):
    name = 'saveon2'
    allowed_domains = ['saveoncannabis.com']
    start_urls = ['https://www.saveoncannabis.com/coupons/']
    page_url = 'https://www.saveoncannabis.com/coupons/%s/'

    def __init__(self, store=None, *args, **kwargs):
        super(Saveon2Spider, self).__init__(*args, **kwargs)
        self.store = store

    def start_requests(self):
        if self.store:
            yield scrapy.Request(url=self.store, callback=self.coupon_parse)
        else:
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        # if not re.findall(r'/coupons/(.+?)/', response.url):
        #     max_page = int(soup.find('ul', class_='pagination').find_all('a')[-1].text)
            # for i in range(2, max_page + 1):
                # yield scrapy.Request(url=self.page_url % i, callback=self.parse)
        coupon_infos = soup.find_all('div', class_='offer-box')
        for coupon_info in coupon_infos:
            store_link = coupon_info.find('ul', class_='bottom-meta').find('a').get('href')
            coupon_link = coupon_info.find('a', class_='show-code').get('href')
            yield scrapy.Request(url=store_link + coupon_link, callback=self.coupon_parse)

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        main_coupon_info = soup.find('div', class_='store-offer-featured')
        main_coupon = CouponItem()
        main_coupon['type'] = 'coupon'
        main_coupon['name'] = main_coupon_info.find('h2').text.strip()
        main_coupon['site'] = 'saveoncannabis.com'
        main_coupon['description'] = ''
        main_coupon['verify'] = True
        main_coupon['link'] = ''
        main_coupon['expire_at'] = main_coupon_info.find('div', class_='deal-countdown-info').text.strip().replace(
            'Expires in: ', '')
        main_coupon['expire_at'] = '' if 'Unlimited Time' in main_coupon['expire_at'] else main_coupon['expire_at']
        main_coupon['coupon_type'] = 'CODE'
        offer_id = main_coupon_info.find('div', class_='featured-coupon-button').find('a').get('data-offer_id')
        main_coupon['final_website'] = get_real_url(
            main_coupon_info.find('div', class_='featured-coupon-button').find('a').get('data-affiliate'))
        main_coupon['store'] = soup.find('section', class_='page-title').find('h1').text.strip()
        main_coupon['store_description'] = ''
        main_coupon['store_category'] = main_coupon_info.find('div', class_='featured-coupon-meta').find(
            'a').text.strip()
        main_coupon['store_website'] = get_domain_url(main_coupon['final_website'])
        main_coupon['store_country'] = 'US'
        main_coupon['store_picture'] = soup.find('div', class_='shop-logo').find('img').get('src')
        main_coupon['store_url_name'] = soup.find('div', class_='shop-logo').find('a').get('href')
        main_coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield scrapy.FormRequest(url='https://www.saveoncannabis.com/wp-admin/admin-ajax.php',
                                 formdata={'action': 'show_code', 'offer_id': offer_id}, callback=self.code_paese,
                                 dont_filter=True, meta={'item': main_coupon})

    def code_paese(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_item = response.meta['item']
        coupon_item['code'] = soup.find('input').get('value')
        yield coupon_item


def get_domain_url(long_url):
    domain = re.findall(r'^(http[s]?://.+?)[/?]', long_url + '/')
    return domain[0] if domain else None


def get_real_url(url, try_count=1):
    if try_count > 3:
        return url
    try:
        rs = requests.get(url, headers=get_header(), timeout=10, verify=False)
        if rs.status_code > 400 and get_domain_url(rs.url) == 'www.offers.com':
            return get_real_url(url, try_count + 1)
        if get_domain_url(rs.url) == get_domain_url(url):
            target_url = re.findall(r'replace\(\'(.+?)\'', rs.content.decode())
            if target_url:
                return target_url[0].replace('\\', '') if re.match(r'http', target_url[0]) else rs.url
            else:
                return rs.url
        else:
            return get_real_url(rs.url)
    except Exception as e:
        print(e)
        return get_real_url(url, try_count + 1)
