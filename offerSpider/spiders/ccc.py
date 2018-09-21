# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup

from offerSpider.items import StoreItem, CouponItem


class CccSpider(scrapy.Spider):
    name = 'ccc'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://cannabiscouponcodes.com/discount-category/cannabis-seeds/',
                  'https://cannabiscouponcodes.com/discount-category/dabbing-tools/',
                  'https://cannabiscouponcodes.com/discount-category/headshop/',
                  'https://cannabiscouponcodes.com/discount-category/vaporizers-2/',
                  'https://cannabiscouponcodes.com/discount-category/growing-equipment/',
                  'https://cannabiscouponcodes.com/discount-category/cbd-2/']

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        counts = soup.find_all('div', class_='result-stat-fig')
        counts = [int(x) for x in counts]
        total_page = int(sum(counts) / 12)
        yield scrapy.Request(url=response.url + '/?fwp_load_more=%s' % total_page, callback=self.coupon_parse)

        pass

    def coupon_parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        coupon_infos = soup.find('div', class_='facetwp-template').find_all('div', class_='coupon-box')
        for coupon_info in coupon_infos:
            expired = coupon_info.find('div', class_='listingexpiry').find('i').text.strip()
            if 'expired' in expired:
                continue
            coupon = CouponItem()
            coupon['type'] = 'coupon'
            coupon['name'] = coupon_info.find('div', class_='listingtitle').find('a').text.strip()
            coupon['site'] = 'cannabiscouponcodes.com'
            coupon['description'] = coupon_info.find('div', class_='listingsexcerpt').find('span').text.strip()
            coupon['verify'] = False
            coupon['link'] = ''
            if 'unknown' in expired:
                coupon['expire_at'] = ''
            else:
                script = coupon_info.find('div', class_='countdowntimer').find('script')

                coupon['expire_at'] = re.findall(r'var dateStr =	"(.+?)";', script)[0]
            coupon['coupon_type'] = 'CODE' if 'Coupon' in coupon_info.find('div', class_='main-deal-button').find(
                'a').text else 'DEAL'

            coupon['code'] = scrapy.Field()
            coupon['final_website'] = scrapy.Field()
            coupon['store'] = scrapy.Field()
            coupon['store_url_name'] = scrapy.Field()
            coupon['store_description'] = scrapy.Field()
            coupon['store_category'] = scrapy.Field()
            coupon['store_website'] = scrapy.Field()
            coupon['store_country'] = scrapy.Field()
            coupon['store_picture'] = scrapy.Field()
            coupon['created_at'] = scrapy.Field()
            coupon['status'] = scrapy.Field()
            coupon['depth'] = scrapy.Field()
        pass
