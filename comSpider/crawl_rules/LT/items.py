# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LTListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    oldprice = scrapy.Field()
    realprice = scrapy.Field()
    favor = scrapy.Field()
    url = scrapy.Field()

class LTDetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    num = scrapy.Field()
    rank = scrapy.Field()
    price_currency = scrapy.Field()
    price_whole = scrapy.Field()
    price_frac = scrapy.Field()
    title = scrapy.Field()
    score = scrapy.Field()
    img = scrapy.Field()
    brand = scrapy.Field()
