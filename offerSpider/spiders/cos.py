# -*- coding: utf-8 -*-
import datetime
import re

import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import CouponItem
from offerSpider.util import get_header


class CosSpider(scrapy.Spider):
    name = 'cos'
    allowed_domains = ['cbdoilusers.com']
    start_urls = ['https://www.cbdoilusers.com/cbd-oil-promo-codes/']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find_all('div', class_='vc_column-inner ')
        for coupon_info in coupon_infos:
            try:
                coupon = CouponItem()
                coupon['type'] = 'coupon'
                coupon['name'] = ''
                coupon['site'] = 'www.cbdoilusers.com'
                code_info = coupon_info.find('h5', class_='vc_custom_heading').text.replace('\n', '')
                code = re.findall(r':(.+?) - ', code_info)
                description = re.findall(r' - (.+?)$', code_info)
                coupon['description'] = description[0] if description else re.findall(r':(.+?)', code_info)[0]
                coupon['verify'] = False
                coupon['link'] = ''
                coupon['expire_at'] = ''
                coupon['code'] = code[0] if code else ''

                coupon['coupon_type'] = 'CODE' if code else 'DEAL'
                coupon['final_website'] = get_real_url(coupon_info.find('a').get('href'))
                coupon['store'] = coupon_info.find('h3',class_='vc_custom_heading').find('a').text.strip()
                coupon['store_url_name'] = coupon_info.find('h3',class_='vc_custom_heading').find('a').get('href')
                coupon['store_description'] = ''
                coupon['store_category'] = 'CBD OIL'
                coupon['store_website'] = get_domain_url(coupon['final_website'])
                coupon['store_country'] = 'US'
                coupon['store_picture'] = coupon_info.find('img').get('src')
                coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield coupon
            except:
                pass
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