# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.images import ImagesPipeline
from .settings import IMAGES_STORE as images_store
from offerSpider.items import StoreItem


class OfferspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class OfferImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, StoreItem):
            image_url = item["logo_url"]
            if "None" not in image_url:
                # 将图片地址提交下载器下载
                yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 下载完成后实现对图片重命名
        image_path = [x['path'] for ok, x in results if ok]
        if len(image_path) > 0:
            os.rename(images_store + "\\" + image_path[0],
                      images_store + "\\" + item["title"] + "\\" + image_path[0])
        return item
