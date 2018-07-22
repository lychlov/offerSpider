# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OfferspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class StoreItem(scrapy.Item):
    type = scrapy.Field()
    logo_url = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    site = scrapy.Field()
    url_name = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    website = scrapy.Field()
    country = scrapy.Field()
    picture = scrapy.Field()
    coupon_count = scrapy.Field()
    created_at = scrapy.Field()
    final_website = scrapy.Field()
    depth = scrapy.Field()
    download_timeout = scrapy.Field()
    download_slot = scrapy.Field()
    download_latency = scrapy.Field()


class CouponItem(scrapy.Item):
    type = scrapy.Field()
    name = scrapy.Field()
    site = scrapy.Field()
    description = scrapy.Field()
    verify = scrapy.Field()
    link = scrapy.Field()
    expire_at = scrapy.Field()
    coupon_type = scrapy.Field()
    code = scrapy.Field()
    final_website = scrapy.Field()
    store = scrapy.Field()
    store_url_name = scrapy.Field()
    store_description = scrapy.Field()
    store_category = scrapy.Field()
    store_website = scrapy.Field()
    store_country = scrapy.Field()
    store_picture = scrapy.Field()
    created_at = scrapy.Field()
    status = scrapy.Field()
    depth = scrapy.Field()
    download_timeout = scrapy.Field()
    download_slot = scrapy.Field()
    download_latency = scrapy.Field()
