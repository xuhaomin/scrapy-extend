# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IP(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mp_ip = scrapy.Field()
    mp_create_time = scrapy.Field()
    mp_status = scrapy.Field()
    mp_id = scrapy.Field()
    mp_protocol = scrapy.Field()

