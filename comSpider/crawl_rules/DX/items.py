# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DXListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()
    sku = scrapy.Field()

class DXDetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    para = scrapy.Field()

