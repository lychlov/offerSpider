# -*- coding: utf-8 -*-
import datetime
import re

import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import CouponItem
from offerSpider.util import get_header


class TstSpider(scrapy.Spider):
    name = 'tst'
    allowed_domains = ['theseedlingtruck.com']
    start_urls = ['http://theseedlingtruck.com/category/cbd-deals/page/2/']
    page_url = 'http://theseedlingtruck.com/category/cbd-deals/page/%s/'
    base_url = 'http://theseedlingtruck.com'

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        max_page = soup.find_all('a', class_='page-numbers')[-2].text.strip()
        for i in range(int(max_page)):
            yield scrapy.Request(url=self.page_url % i, callback=self.list_parse)
        coupon_infos = soup.find_all('article')
        for coupon_info in coupon_infos:
            link = coupon_info.find('h2').find('a').get('href')
            yield scrapy.Request(url=link, callback=self.coupon_parse)
        pass

    def list_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find_all('article')
        for coupon_info in coupon_infos:
            link = coupon_info.find('a').get('href')
            yield scrapy.Request(url=link, callback=self.coupon_parse)

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        button = soup.find('button')
        coupon = CouponItem()
        coupon['type'] = 'coupon'
        coupon['name'] = button.get('title')
        coupon['site'] = 'theseedlingtruck.com'
        coupon['description'] = button.get('data-description')
        coupon['verify'] = False
        coupon['link'] = ''
        coupon['expire_at'] = ''
        coupon['coupon_type'] = 'CODE' if 'code' in button.get('data-classes') else 'DEAL'
        coupon['code'] = button.get('data-code')
        coupon['final_website'] = get_real_url(self.base_url + button.get('data-url'))
        coupon['store'] = button.get('data-url')
        coupon['store_url_name'] = self.base_url + button.get('data-url')
        coupon['store_description'] = ''
        coupon['store_category'] = 'CDB DEALS'
        coupon['store_website'] = get_domain_url(coupon['final_website'])
        coupon['store_country'] = 'US'
        coupon['store_picture'] = button.get('data-image')
        coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield coupon


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
