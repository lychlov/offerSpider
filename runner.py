# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     runner
   Description :
   Author :       Lychlov
   date：          2018/7/20
-------------------------------------------------
   Change Activity:
                   2018/7/20:
-------------------------------------------------
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'offer' is the name of one of the spiders of the project.
process.crawl('offer', domain='www.offer.com')
process.start() # the script will block here until the crawling is finished