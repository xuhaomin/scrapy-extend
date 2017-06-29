#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-27 09:01:35
# @Author  : xuhaomin
# @Version : python3.6
import re
import json

from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle


from comSpider.config import *
from utils.log import *
from utils.spider import CommonSpider


class globalSpider(CommonSpider):
    name = spider_name
    allowed_domains = domains
    start_urls = start_urls

    item_extractor = item_extractor
    crawl_item = crawl_item

    def parse(self, response):
        info('Parse '+response.url)
        items = self.parse_with_rules(
            response, self.item_extractor, crawl_item)

        # dump data for test
        res = {}
        with open(file_for_test, 'w+') as f:
            for k, v in items.items():
                res[k] = v
            json.dump(res, f)
