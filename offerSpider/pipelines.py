# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy.pipelines.images
from .settings import IMAGES_STORE as images_store
from offerSpider.items import StoreItem


class OfferspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class OfferImagePipeline(scrapy.pipelines.images.ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, StoreItem):
            image_url = item["logo_url"]
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 下载完成后实现对图片重命名
        image_path = [x['path'] for ok, x in results if ok]
        file_path = images_store + "/" + item['site']+'/'+item["title"]
        if not os.path.exists(file_path):
            # 如果不存在则创建目录
            #  创建目录操作函数
            os.makedirs(file_path)
        if len(image_path) > 0:
            os.rename(images_store + "/" + image_path[0],
                      images_store + "/" + item['site']+'/'+item["title"] + "."+image_path[0].split('.')[-1])
        return item
