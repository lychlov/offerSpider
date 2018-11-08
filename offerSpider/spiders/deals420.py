# -*- coding: utf-8 -*-
import datetime

import requests
import scrapy
from bs4 import BeautifulSoup
import re

from offerSpider.items import CouponItem
from offerSpider.util import get_header


class Deals420Spider(scrapy.Spider):
    name = 'deals420'
    allowed_domains = ['420.deals']
    start_urls = ['https://420.deals/discount-codes-for/cannabis-seeds/?fwp_paged=1',
                  'https://420.deals/discount-codes-for/smoking-gear/?fwp_paged=1',
                  'https://420.deals/discount-codes-for/dabbing-gear/?fwp_paged=1',
                  'https://420.deals/discount-codes-for/vaporizers/?fwp_paged=1',
                  'https://420.deals/discount-codes-for/growing-gear/?fwp_paged=1']

    def __init__(self, store=None, *args, **kwargs):
        super(Deals420Spider, self).__init__(*args, **kwargs)
        if '?fwp_paged=1' in store:
            self.store = store
        else:
            self.store = store + '?fwp_paged=1'

    def start_requests(self):
        if self.store:
            yield scrapy.Request(url=self.store, callback=self.parse)
        else:
            for url in self.start_urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        html = response.body
        category = re.findall(r'discount-codes-for/(.+?)/', response.url)[0] if re.findall(r'discount-codes-for/(.+?)/',
                                                                                           response.url) else ''
        soup = BeautifulSoup(html, 'lxml')
        exit_count = soup.find('b', class_='num').text
        if exit_count != '0':
            current_page = re.findall(r'fwp_paged=(.+?)', response.url)[0]
            next_url = response.url.replace(current_page, str(int(current_page) + 1))
            yield scrapy.Request(url=next_url, callback=self.parse)
        offers = soup.find_all('div', class_='itemdata')
        for offer in offers:
            expired = offer.find('span', class_='wlt_shortcodes_expiry_date').text
            if 'expired' in expired:
                continue
            coupon = CouponItem()
            coupon['type'] = 'coupon'
            coupon['name'] = offer.find('div', class_='titletext').find('span').text.strip()
            coupon['site'] = '420.deals'
            coupon['description'] = offer.find('div', class_='excerpttext').find('p').text.strip()
            coupon['verify'] = False
            button = offer.find('div', class_='clicktoreveal')

            # coupon['link'] = offer.find('div', class_='titletext').find('a').get('href')

            coupon['link'] = ''
            coupon['expire_at'] = ''

            coupon['coupon_type'] = 'DEAL' if 'Deal' in button.text else 'CODE'
            coupon['code'] = button.find('div', class_='code').text.strip() if coupon['coupon_type'] != 'DEAL' else ''
            link = button.find('a').get('href') if coupon['coupon_type'] == 'DEAL' else re.findall(r"href='(.+?)';",
                                                                                                   button.next_sibling.next_sibling.text)[
                0]
            coupon['final_website'] = get_real_url(link)
            store_info = offer.find('span', class_='wlt_shortcode_store')
            coupon['store'] = store_info.find('a').text.strip()
            coupon['store_url_name'] = store_info.find('a').get('href')
            coupon['store_description'] = ''
            coupon['store_category'] = category
            coupon['store_website'] = get_domain_url(coupon['final_website'])
            coupon['store_country'] = 'US'
            coupon['store_picture'] = offer.find('img').get('src')
            coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # coupon['status'] = scrapy.Field()
            # coupon['depth'] = scrapy.Field()
            # coupon['download_timeout'] = scrapy.Field()
            # coupon['download_slot'] = scrapy.Field()
            # coupon['download_latency'] = scrapy.Field()
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
