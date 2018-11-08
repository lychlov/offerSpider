# -*- coding: utf-8 -*-
import re

import datetime
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import CouponItem, StoreItem
from offerSpider.util import get_header


class VapingSpider(scrapy.Spider):
    name = 'vaping'
    allowed_domains = ['vaping.coupons']
    start_urls = ['https://vaping.coupons/stores/']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        stores_list = soup.find_all('ul', class_='stores')
        for stores in stores_list:
            for store in stores.find_all('li'):
                store_link = store.find('a').get('href')
                total = re.findall(r'\((.+?)\)', str(store))[0]
                if total != 0:
                    for i in range(int(int(total) / 10) + 1):
                        yield scrapy.Request(url=store_link + 'page/%s/' % str(i + 1), callback=self.coupon_parse)

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find_all('div', class_='type-coupon')
        store_info =soup.find('div',class_='store')
        for coupon_info in coupon_infos:
            coupon = CouponItem()
            if coupon_info.find('p', class_='expired_msg'):
                continue

            coupon['type'] = 'coupon'
            # coupon['name'] = coupon_info.find('h3', class_='entry-title').find('a').get('title')
            coupon['name'] = coupon_info.find('h3', class_='entry-title').find('a').text.strip()
            coupon['site'] = 'vaping.coupons'
            coupon['description'] = ''
            coupon['verify'] = False
            coupon['link'] = ''
            coupon['expire_at'] = coupon_info.find('li', class_='expire').get('datetime')
            button = coupon_info.find('div', class_='link-holder').find('a')
            coupon['coupon_type'] = 'DEAL' if 'Redeem' in button.get('data-clipboard-text') else 'CODE'
            coupon['code'] = button.get('data-clipboard-text') if coupon['coupon_type'] == 'CODE' else ''
            coupon['final_website'] = get_real_url(button.get('href'))
            coupon['store'] = store_info.find('h1').text.strip()
            coupon['store_url_name'] = button.get('href')
            coupon['store_description'] = store_info.find('div',class_='desc').text.strip()
            coupon['store_category'] = coupon_info.find('p',class_='tag').text.replace('Tags:','').strip()
            coupon['store_website'] = get_domain_url(coupon['final_website'])
            coupon['store_country'] = 'US'
            coupon['store_picture'] = store_info.find('img').get('src')
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
