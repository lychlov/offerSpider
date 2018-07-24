# -*- coding: utf-8 -*-
import datetime
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import StoreItem, CouponItem, CategoryItem
from offerSpider.util import get_header
import re


def get_domin_url(long_url):
    domin = re.findall(r'^(http[s]?://.+?)[/?]', long_url)
    return domin[0] if domin else None
    pass


class OfferSpider(scrapy.Spider):
    name = 'offer'
    allowed_domains = ['offers.com']
    start_urls = ['https://www.offers.com/stores/', 'https://www.offers.com/c/']
    base_url = 'https://www.offers.com'
    code_url = 'https://www.offers.com/exit/modal/offerid/code_id/?view_buoy=long_id'

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        if response.url == self.start_urls[0]:
            letters = soup.find('div', class_='letters').find_all('a')
            for letter in letters:
                href = self.base_url + letter.get('href')
                yield scrapy.Request(href, callback=self.letter_page_parse)
        elif response.url == self.start_urls[1]:
            top_categories = soup.find_all('div', class_='category list')
            for top_category in top_categories:
                categries = top_category.find_all('a')
                for category in categries:
                    href = self.base_url + category.get('href')
                    yield scrapy.Request(href, callback=self.category_page_parse)
        pass

    def category_page_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        category_item = CategoryItem()
        category_item['type'] = 'category'
        category_item['name'] = soup.find('div', id='middle-info').find('strong').text.strip()
        category_item['url_name'] = response.url.split('/')[-2]
        category_item['description'] = soup.find('div', id='middle-info').find('p').text.strip()
        category_item['site'] = 'offers.com'
        category_item['icon_code'] = 'icon-christmas-001'
        category_item['icon_color'] = 'primary'
        category_item['status'] = '0'
        # category_item['depth = scrapy.Field()
        # category_item['download_timeout = scrapy.Field()
        # category_item['download_slot = scrapy.Field()
        # category_item['download_latency = scrapy.Field()
        yield category_item

    def letter_page_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        stores = []
        try:
            stores = soup.find('div', class_='stores-by-letter').find_all('a')
        except:
            print(response.url)
        for store in stores:
            href = self.base_url + store.get('href')
            yield scrapy.Request(href, callback=self.store_page_parse)
        pass

    def store_page_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        store_item = StoreItem()
        # 处理字段定位
        # store
        store_item['type'] = 'store'
        store_item['logo_url'] = 'https:' + soup.find('div', id='header-logo').a.img.get('src')
        store_item['title'] = soup.find('div', id='filterable-header').find('strong').text.strip()
        store_item['name'] = store_item['title']
        store_item['site'] = 'offers'
        store_item['url_name'] = response.url.split('/')[-2]
        store_item['description'] = soup.find('div', id='company-information').find('p').text
        store_item['category'] = soup.find_all('a', itemprop='item')[-1].find('span').text
        store_item['website'] = get_real_url(self.base_url + soup.find('div', id='header-logo').a.get('href'))
        store_item['country'] = "US"
        store_item['picture'] = scrapy.Field()
        store_item['coupon_count'] = soup.find('div', id='merchant-stats').find('tr').find('span').text
        store_item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        store_item['final_website'] = get_domin_url(store_item['website'])
        if store_item['final_website'] == '' or store_item['final_website'] is None or store_item[
            'final_website'] == '#' or store_item['final_website'] == 'https://www.offers.com':
            print(store_item['final_website'])
        # coupon
        for offer in soup.find_all('div', class_='offerstrip'):
            coupon_item = CouponItem()
            coupon_item['type'] = 'coupon'
            coupon_item['name'] = offer.find('div', class_='offer-info').find('a').text
            coupon_item['site'] = 'offers'
            coupon_item['description'] = coupon_item['name']
            try:
                coupon_item['verify'] = 'Y' if offer.find('span', class_='verified').find(
                    'strong').text == "Verified" else "N"
            except:
                coupon_item['verify'] = 'N'
            coupon_item['link'] = self.base_url + offer.find('a').get('href')
            coupon_item['expire_at'] = None
            try:
                div = offer.find('div', class_='badge-text')
                span = offer.find('span', class_='dolphin flag')
                coupon_item['coupon_type'] = div.text.strip() if div else span.text.strip()
            except:
                coupon_item['coupon_type'] = offer.find('div', class_='discount').text.strip()
            if 'code' in coupon_item['coupon_type']:
                data_offer_id = offer.get('data-offer-id')
                long_id = coupon_item['link'].split('/')[-2]
                code_get_url = self.code_url.replace('code_id', data_offer_id).replace('long_id', long_id)
                res = requests.get(code_get_url, headers=get_header(), verify=False)
                code = re.findall(r'<div class="coupon-code">(.+?)</div>', res.content.decode())
                coupon_item['code'] = code[0] if code else ''
                coupon_item['coupon_type'] = "CODE"
            else:
                coupon_item['coupon_type'] = "DEAL"
                coupon_item['code'] = ''
            coupon_item['final_website'] = store_item['final_website']
            coupon_item['store'] = store_item['title']
            coupon_item['store_url_name'] = store_item['url_name']
            coupon_item['store_description'] = store_item['description']
            coupon_item['store_category'] = store_item['category']
            coupon_item['store_website'] = store_item['website']
            coupon_item['store_country'] = "US"
            coupon_item['store_picture'] = store_item['logo_url']
            coupon_item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            coupon_item['status'] = '0'
            # coupon_item['depth'] = scrapy.Field()
            # coupon_item['download_timeout'] = scrapy.Field()
            # coupon_item['download_slot'] = scrapy.Field()
            # coupon_item['download_latency'] = scrapy.Field()
            yield coupon_item
        yield store_item
        pass


def get_real_url(url, try_count=1):
    if try_count > 3:
        return url
    try:
        rs = requests.get(url, headers=get_header(), timeout=10, verify=False)
        if rs.status_code > 400:
            return get_real_url(url, try_count + 1)
        if get_domin_url(rs.url) == get_domin_url(url):
            target_url = re.findall(r'replace\(\'(.+?)\'', rs.content.decode())
            if target_url:
                return target_url[0].replace('\\', '') if re.match(r'http', target_url[0]) else rs.url
        else:
            return get_real_url(rs.url)
    except Exception as e:
        print(e)
        return get_real_url(url, try_count + 1)
