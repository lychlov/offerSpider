# -*- coding: utf-8 -*-
import re

import datetime
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import StoreItem, CouponItem
from offerSpider.util import get_header, get_cookies


class CccSpider(scrapy.Spider):
    name = 'ccc'
    store_info_cache = {}
    allowed_domains = ['cannabiscouponcodes.com']
    start_urls = ['https://cannabiscouponcodes.com/']
    cat_urls = ['https://cannabiscouponcodes.com/discount-category/cannabis-seeds/',
                'https://cannabiscouponcodes.com/discount-category/dabbing-tools/',
                'https://cannabiscouponcodes.com/discount-category/headshop/',
                'https://cannabiscouponcodes.com/discount-category/vaporizers-2/',
                'https://cannabiscouponcodes.com/discount-category/growing-equipment/',
                'https://cannabiscouponcodes.com/discount-category/cbd-2/']
    base_url = 'https://cannabiscouponcodes.com/'
    base_code_url = 'https://cannabiscouponcodes.com/?core_aj=1&action=couponform&couponid=%s'
    cookie = None

    def start_requests(self):
        for url in self.cat_urls:
            yield scrapy.Request(url=url, callback=self.parse_bak)

    def parse(self, response):
        base64_crypto = re.findall(r"S='(.+?)'", response.body.decode())[0]
        self.cookie = get_cookies(base64_crypto)
        for url in self.cat_urls:
            yield scrapy.Request(url=url, callback=self.parse_bak, cookies=self.cookie)

    def parse_bak(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        counts = soup.find_all('div', class_='result-stat-fig')
        counts = [int(x.text) for x in counts]
        total_page = int(sum(counts) / 12)
        # total_page = 2
        yield scrapy.Request(url=response.url + '?fwp_load_more=%s' % total_page, callback=self.coupon_parse)
        pass

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find('div', class_='facetwp-template').find_all('div', class_='coupon-box')
        for coupon_info in coupon_infos:
            expired = coupon_info.find('div', class_='listingexpiry').text.strip()
            if 'expired' in expired:
                continue
            coupon = CouponItem()
            coupon['type'] = 'coupon'
            try:
                coupon['name'] = coupon_info.find('div', class_='listingtitle').find('a').text.strip()
            except:
                coupon['name'] = ''
            coupon['site'] = 'cannabiscouponcodes.com'
            coupon['description'] = coupon_info.find('div', class_='listingsexcerpt').find('span').text.strip()
            coupon['verify'] = False
            coupon['link'] = ''
            if 'unknown' in expired:
                coupon['expire_at'] = ''
            else:
                script = coupon_info.find('div', class_='countdowntimer').find('script')

                coupon['expire_at'] = re.findall(r'var dateStr \=\t"(.+?)";', str(script))[0]
            coupon['coupon_type'] = 'CODE' if 'Coupon' in coupon_info.find('div', class_='main-deal-button').find(
                'a').text else 'DEAL'

            coupon['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            coupon['store_country'] = 'US'
            coupon['store_picture'] = coupon_info.find('div', class_='coupon-box-logo').find('img').get('src')
            coupon['store_category'] = re.findall(r'discount-category/(.+?)/', response.url)[0]
            coupon['store'] = coupon_info.find('div', class_='listingsstore').find('a').text.strip()
            coupon['store_url_name'] = coupon_info.find('div', class_='listingsstore').find('a').get('href')
            coupon['store_description'] = ''

            coupon_id = coupon_info.find('div', class_='main-deal-button').find('a').get('data-couponid')
            code_get_url = self.base_code_url % coupon_id
            yield scrapy.Request(url=code_get_url, callback=self.code_parse,
                                 meta={'item': coupon})

    def code_parse(self, response):
        html = response.body.decode()
        coupon_item = response.meta['item']
        if coupon_item['coupon_type'] == 'CODE':
            code = re.findall(r'id="copybtn">(.+?)</div>', html)[0]
            coupon_item['code'] = code
        else:
            coupon_item['code'] = ''

        out_link = re.findall(r'(https://cannabiscouponcodes.com/out/.+?/link/)', html)[0]
        if out_link in self.store_info_cache.keys():
            coupon_item['final_website'] = self.store_info_cache[out_link].get('final_website', '')
            coupon_item['store_website'] = self.store_info_cache[out_link].get('store_website', '')
            yield coupon_item
        else:
            yield scrapy.Request(url=out_link, callback=self.out_link_parse, meta={'item': coupon_item,
                                                                                   'out_link': out_link})
        pass

    def out_link_parse(self, response):
        html = response.body.decode()
        coupon_item = response.meta['item']
        out_link = response.meta['out_link']
        coupon_item['final_website'] = response.url
        coupon_item['store_website'] = get_domain_url(response.url)
        self.store_info_cache[out_link] = {'final_website': coupon_item['final_website'],
                                           'store_website': coupon_item['store_website']}
        yield coupon_item
        pass

    def store_parse(self, response):
        store = StoreItem()

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
