# -*- coding: utf-8 -*-
import datetime
import re

import requests
import scrapy
from bs4 import BeautifulSoup
from offerSpider.items import CouponItem
from offerSpider.util import get_header


class PuregreenlivingSpider(scrapy.Spider):
    name = 'puregreenliving'
    base_url = 'https://puregreenliving.com'
    allowed_domains = ['puregreenliving.com']
    start_urls = ['https://puregreenliving.com/category/cbd-deals',
                  'https://puregreenliving.com/category/pet-cbd-deals',
                  'https://puregreenliving.com/category/vaporizer-discount-codes',
                  'https://puregreenliving.com/category/ecig-deals',
                  'https://puregreenliving.com/category/420-seed-deals',
                  'https://puregreenliving.com/category/420-deals',
                  'https://puregreenliving.com/category/weed-delivery-deals',
                  'https://puregreenliving.com/category/educational-deals']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        deals = soup.find_all('article')
        for deal in deals:
            if 'Review' not in deal.find('h2', class_='title').find('a').text:
                deal_url = deal.find('h2', class_='title').find('a').get('href')
                yield scrapy.Request(url=deal_url, callback=self.coupon_parse)
        pass

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')

        coupon_info = soup.find('div', class_='coupon-popup')
        button = coupon_info.find('button')
        coupon = CouponItem()
        coupon['type'] = 'coupon'
        coupon['name'] = button.get('title')
        coupon['site'] = 'puregreenliving.com'
        coupon['description'] = button.get('data-description')
        coupon['verify'] = False
        coupon['link'] = ''
        coupon['expire_at'] = ''
        coupon['coupon_type'] = 'CODE'
        coupon['code'] = button.get('data-code')
        link = self.base_url + button.get('data-url')

        coupon['final_website'] = get_real_url(link)
        # coupon['store'] = button.get('data-url').replace('/', '')
        coupon['store'] = soup.find('div', class_='post-header-title').find('span', class_='post-title')
        coupon['store'] = coupon['store'].text.replace(' Coupon Codes', '') if coupon['store'] else button.get(
            'data-url').replace('/', '')
        coupon['store_url_name'] = link
        coupon['store_description'] = ''
        coupon['store_category'] = soup.find('span', class_='term-badge').find('a').text.strip()
        coupon['store_website'] = get_domain_url(coupon['final_website'])
        coupon['store_country'] = 'US'
        coupon['store_picture'] = button.get('data-image')
        coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # coupon['status'] = scrapy.Field()
        # depth = scrapy.Field()
        # download_timeout = scrapy.Field()
        # download_slot = scrapy.Field()
        # download_latency = scrapy.Field()
        yield coupon
        pass


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
