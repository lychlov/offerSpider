# -*- coding: utf-8 -*-
import re

import datetime
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.util import get_header
from offerSpider.items import CouponItem


class SockSpider(scrapy.Spider):
    name = 'sock'
    allowed_domains = ['couponsock.com']
    start_urls = ['http://www.couponsock.com/search/?q=cbd']
    base_url = 'http://www.couponsock.com'

    def parse(self, response):
        html = response.body.decode()
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find('div', class_='index_top_box').find_all('div', class_='media')
        for coupon_info in coupon_infos:
            try:
                coupon = CouponItem()
                coupon['type'] = 'coupon'
                coupon['name'] = coupon_info.find('h3', class_='each_box_header').text.strip()
                coupon['site'] = 'www.couponsock.com'
                coupon['description'] = coupon_info.find('p').text.strip()
                coupon['verify'] = False
                coupon['link'] = ''
                coupon['coupon_type'] = 'CODE'
                coupon['expire_at'] = ''
                coupon['code'] = coupon_info.find('div', class_='code_button').find('a').get('code')
                coupon['final_website'] = get_real_url(
                    self.base_url + coupon_info.find('div', class_='code_button').find('a').get('href'))
                coupon['store'] = coupon_info.find('p', class_='more_p_a').find('a').get('href').replace('/store-coupons/',
                                                                                                         '')
                coupon['store_url_name'] = self.base_url + coupon_info.find('p', class_='more_p_a').find('a').get('href')
                coupon['store_description'] = ''
                coupon['store_category'] = ''
                coupon['store_website'] = get_domain_url(coupon['final_website'])
                coupon['store_country'] = 'US'
                coupon['store_picture'] = coupon_info.find('img').get('src')
                coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield coupon
            except Exception as e:
                print(e)
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
