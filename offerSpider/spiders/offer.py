# -*- coding: utf-8 -*-
import datetime
import requests
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import StoreItem, CouponItem
from offerSpider.util import get_header
import re


def loacte_items(soup):
    store_item = StoreItem()
    coupon_item = CouponItem()
    # store
    store_item['type'] = scrapy.Field()
    store_item['logo_url'] = scrapy.Field()
    store_item['title'] = scrapy.Field()
    store_item['name'] = scrapy.Field()
    store_item['site'] = scrapy.Field()
    store_item['url_name'] = scrapy.Field()
    store_item['description'] = scrapy.Field()
    store_item['category'] = scrapy.Field()
    store_item[' website'] = scrapy.Field()
    store_item['country'] = scrapy.Field()
    store_item['picture'] = scrapy.Field()
    store_item['coupon_count'] = scrapy.Field()
    store_item['created_at'] = scrapy.Field()
    store_item['final_website'] = scrapy.Field()
    store_item['depth'] = scrapy.Field()
    # coupon
    coupon_item['type'] = scrapy.Field()
    coupon_item['name'] = scrapy.Field()
    coupon_item['site'] = scrapy.Field()
    coupon_item['description'] = scrapy.Field()
    coupon_item['verify'] = scrapy.Field()
    coupon_item['link'] = scrapy.Field()
    coupon_item['expire_at'] = scrapy.Field()
    coupon_item['coupon_type'] = scrapy.Field()
    coupon_item['code'] = scrapy.Field()
    coupon_item['final_website'] = scrapy.Field()
    coupon_item['store'] = scrapy.Field()
    coupon_item['store_url_name'] = scrapy.Field()
    coupon_item['store_description'] = scrapy.Field()
    coupon_item['store_category'] = scrapy.Field()
    coupon_item['store_website'] = scrapy.Field()
    coupon_item['store_country'] = scrapy.Field()
    coupon_item['store_picture'] = scrapy.Field()
    coupon_item['created_at'] = scrapy.Field()
    coupon_item['status'] = scrapy.Field()
    coupon_item['depth'] = scrapy.Field()
    coupon_item['download_timeout'] = scrapy.Field()
    coupon_item['download_slot'] = scrapy.Field()
    coupon_item['download_latency'] = scrapy.Field()
    pass


def get_domin_url(long_url):
    domin = re.findall(r'^(http[s]?://.+?)/', long_url)
    return domin[0] if domin else None
    pass


class OfferSpider(scrapy.Spider):
    name = 'offer'
    allowed_domains = ['offers.com']
    start_urls = ['https://www.offers.com/stores/']
    base_url = 'https://www.offers.com'
    code_url = 'https://www.offers.com/exit/modal/offerid/code_id/?view_buoy=long_id'

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        letters = soup.find('div', class_='letters').find_all('a')
        for letter in letters:
            href = self.base_url + letter.get('href')
            yield scrapy.Request(href, callback=self.letter_page_parse)
        pass

    def letter_page_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
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
        coupon_item = CouponItem()
        # 处理字段定位
        # store
        store_item['type'] = 'store'
        store_item['logo_url'] = 'https:' + soup.find('div', id='header-logo').a.img.get('src')
        store_item['title'] = soup.find('div', id='filterable-header').find('strong').text
        store_item['name'] = store_item['title']
        store_item['site'] = 'offers.com'
        store_item['url_name'] = response.url
        store_item['description'] = soup.find('div', id='company-information').find('p').text
        store_item['category'] = soup.find_all('a', itemprop='item')[-1].find('span').text
        store_item['website'] = get_real_url(self.base_url + soup.find('div', id='header-logo').a.get('href'))
        store_item['country'] = "US"
        store_item['picture'] = scrapy.Field()
        store_item['coupon_count'] = soup.find('div', id='merchant-stats').find('tr').find('span').text
        store_item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        store_item['final_website'] = get_domin_url(store_item['website'])

        # coupon
        for offer in soup.find_all('div', class_='offerstrip'):
            coupon_item['type'] = 'coupon'
            coupon_item['name'] = offer.find('div', class_='offer-info').find('a').text
            coupon_item['site'] = 'offers.com'
            coupon_item['description'] = coupon_item['name']
            try:
                coupon_item['verify'] = 'Y' if offer.find('span', class_='verified').find('strong').text=="Verified" else "N"
            except:
                print(offer)
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
                res = requests.get(code_get_url, headers=get_header(),verify=False)
                code = re.findall(r'<div class="coupon-code">(.+?)</div>', res.content.decode())
                coupon_item['code'] = code[0] if code else ''
            else:
                coupon_item['code'] = ''
            coupon_item['final_website'] = store_item['final_website']
            coupon_item['store'] = store_item['title']
            coupon_item['store_url_name'] = response.url
            coupon_item['store_description'] = store_item['description']
            coupon_item['store_category'] = store_item['category']
            coupon_item['store_website'] = store_item['website']
            coupon_item['store_country'] = "US"
            # coupon_item['store_picture'] = scrapy.Field()
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
        rs = requests.get(url, headers=get_header(), timeout=10)
        if rs.status_code > 400:
            return get_real_url(url, try_count + 1)
        if get_domin_url(rs.url) == get_domin_url(url):
            target_url = re.findall(r'replace\(\'(.+?)\'', rs.content.decode())
            return target_url[0].replace('\\', '') if target_url else rs.url
        else:
            return get_real_url(rs.url)
    except:
        return get_real_url(url, try_count + 1)
