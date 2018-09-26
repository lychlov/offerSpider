# # -*- coding: utf-8 -*-
# import re
#
# import requests
# import scrapy
# from bs4 import BeautifulSoup
#
# from offerSpider.util import get_header
# from offerSpider.items import CouponItem
#
#
# class SaveonSpider(scrapy.Spider):
#     name = 'saveon'
#     allowed_domains = ['saveoncannabis.com']
#     start_urls = ['https://www.saveoncannabis.com/stores']
#     page_url = 'https://www.saveoncannabis.com/stores/%s/'
#
#     def parse(self, response):
#         html = response.body
#         soup = BeautifulSoup(html, 'lxml')
#         if not re.findall(r'/stores/(.+?)/', response.url):
#             max_page = int(soup.find('ul', class_='page-numbers').find('a').text)
#             for i in range(2, max_page + 1):
#                 yield scrapy.Request(url=self.page_url % i, callback=self.parse)
#         stores = soup.find_all('div', class_='store-logo')
#         for store in stores:
#             link = store.find('a').get('href')
#             yield scrapy.Request(url=link, callback=self.store_parse)
#         pass
#
#     def store_parse(self, response):
#         html = response.body
#         soup = BeautifulSoup(html, 'lxml')
#         main_coupon_info = soup.find('div', class_='store-offer-featured')
#         if main_coupon_info:
#             main_coupon = CouponItem()
#             main_coupon['type'] = 'coupon'
#             main_coupon['name'] = main_coupon_info.find('h2').text.strip()
#             main_coupon['site'] = 'saveoncannabis.com'
#             main_coupon['description'] = ''
#             main_coupon['verify'] = True
#             main_coupon['link'] = ''
#             main_coupon['expire_at'] = main_coupon_info.find('div',class_='deal-countdown-info').text.strip().replace('Expires in: ','')
#
#             main_coupon['coupon_type'] = 'CODE'
#
#             main_coupon['code'] = ''
#             main_coupon['final_website'] = ''
#             main_coupon['store'] = ''
#             main_coupon['store_url_name'] = ''
#             main_coupon['store_description'] = ''
#             main_coupon['store_category'] = ''
#             main_coupon['store_website'] = ''
#             main_coupon['store_country'] = ''
#             main_coupon['store_picture'] = ''
#             main_coupon['created_at'] = ''
#             main_coupon['status'] = ''
#             main_coupon['depth'] = ''
#             main_coupon['download_timeout'] = ''
#             main_coupon['download_slot'] = ''
#             main_coupon['download_latency'] = ''
#             yield main_coupon
#
#         coupon_infos = soup.find('div', class_='coupons-other').find_all('div', class_='white-block')
#         if coupon_infos:
#             for coupon_info in coupon_infos:
#                 coupon = CouponItem()
#                 coupon['type'] = 'coupon'
#                 coupon['name'] = ''
#                 coupon['site'] = ''
#                 coupon['description'] = ''
#                 coupon['verify'] = ''
#                 coupon['link'] = ''
#                 coupon['expire_at'] = ''
#                 coupon['coupon_type'] = ''
#                 coupon['code'] = ''
#                 coupon['final_website'] = ''
#                 coupon['store'] = ''
#                 coupon['store_url_name'] = ''
#                 coupon['store_description'] = ''
#                 coupon['store_category'] = ''
#                 coupon['store_website'] = ''
#                 coupon['store_country'] = ''
#                 coupon['store_picture'] = ''
#                 coupon['created_at'] = ''
#                 coupon['status'] = ''
#                 coupon['depth'] = ''
#                 coupon['download_timeout'] = ''
#                 coupon['download_slot'] = ''
#                 coupon['download_latency'] = ''
#                 yield coupon
#         pass
#
#
# def get_domain_url(long_url):
#     domain = re.findall(r'^(http[s]?://.+?)[/?]', long_url + '/')
#     return domain[0] if domain else None
#
#
# def get_real_url(url, try_count=1):
#     if try_count > 3:
#         return url
#     try:
#         rs = requests.get(url, headers=get_header(), timeout=10, verify=False)
#         if rs.status_code > 400 and get_domain_url(rs.url) == 'www.offers.com':
#             return get_real_url(url, try_count + 1)
#         if get_domain_url(rs.url) == get_domain_url(url):
#             target_url = re.findall(r'replace\(\'(.+?)\'', rs.content.decode())
#             if target_url:
#                 return target_url[0].replace('\\', '') if re.match(r'http', target_url[0]) else rs.url
#             else:
#                 return rs.url
#         else:
#             return get_real_url(rs.url)
#     except Exception as e:
#         print(e)
#         return get_real_url(url, try_count + 1)
