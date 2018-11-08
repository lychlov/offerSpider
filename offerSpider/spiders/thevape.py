# -*- coding: utf-8 -*-
import re

import datetime
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import CouponItem
from offerSpider.util import get_header


class ThevapeSpider(scrapy.Spider):
    name = 'thevape'
    allowed_domains = ['thevape.guide']
    start_urls = ['https://thevape.guide/coupon-codes/#']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find('div', class_='templatera_shortcode').find_all('div',class_='centered-container')[2:-1]
        for coupon_info in coupon_infos:
            coupon = CouponItem()
            coupon['type'] = 'coupon'
            coupon['name'] = coupon_info.find_all('p')[1].text.strip()
            coupon['site'] = 'thevape.guide'
            coupon['description'] = re.findall(r'<p style="text-align: center;">(.+?)</p>', str(coupon_info))[1]
            coupon['verify'] = False
            coupon['link'] = ''
            coupon['expire_at'] = ''
            coupon['coupon_type'] = 'CODE'
            coupon['code'] = coupon_info.find('span').text.strip()
            coupon['final_website'] = get_real_url(coupon_info.find('a').get('href'))
            coupon['store'] = coupon_info.find_all('p')[0].text.strip()
            coupon['store_url_name'] = coupon_info.find('a').get('href')
            coupon['store_description'] = ''
            coupon['store_category'] = ''
            coupon['store_website'] = get_domain_url(coupon['final_website'])
            coupon['store_country'] = 'US'
            coupon['store_picture'] = ''
            coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
