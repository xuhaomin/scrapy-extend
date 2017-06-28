# coding: utf-8

import re
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.spiders import CrawlSpider


from .log import *


'''
parse_with_rules 返回值为单个item
其中 item key 继承自配置文件中crawl_item的自定义item
          value 来自于item_extractor遍历dom树后的结果，数据结构为list，每一个叶子节点extract的值作为元素
'''


class CommonSpider(CrawlSpider):

    auto_join_text = False
    ''' # item_extractor example:
    item_extractor = {
        'css': {
            '.zm-profile-header': {
                '.zm-profile-header-main': {
                    '__use':'dump',
                    'name':'.title-section .name::text',
                    'sign':'.title-section .bio::text',
                    'location':'.location.item::text',
                    'business':'.business.item::text',
                    'employment':'.employment.item::text',
                    'position':'.position.item::text',
                    'education':'.education.item::text',
                    'education_extra':'.education-extra.item::text',
                }, 
                '.zm-profile-header-operation': {
                    '__use':'dump',
                    'agree':'.zm-profile-header-user-agree strong::text',
                    'thanks':'.zm-profile-header-user-thanks strong::text',
                }, 
                '.profile-navbar': {
                    '__use':'dump',
                    'asks':'a[href*=asks] .num::text',
                    'answers':'a[href*=answers] .num::text',
                    'posts':'a[href*=posts] .num::text',
                    'collections':'a[href*=collections] .num::text',
                    'logs':'a[href*=logs] .num::text',
                },
            }, 
            '.zm-profile-side-following': {
                '__use':'dump',
                'followees':'a.item[href*=followees] strong::text',
                'followers':'a.item[href*=followers] strong::text',
            }
        },
        'xpath':{
            '//div[@id="centerCol"]': {
                '__use': 'dump',
                'title': './/span[@id="productTitle"]/text()',
                'star': './/span[@id="acrPopover"]/@title',
                'price': './/span[@id="priceblock_ourprice"]/text()',
            },
        },
    }
    '''
    # 将extractor遍历的item保存在数组items作为返回值

    def item_selector(self, sel, query, method):
        '''
        通过method变量来选择使用的遍历方法，目前支持css选择器，xpath选择器和正则方法
        '''
        if method == 'xpath':
            return sel.xpath(query)
        elif method == 'css':
            return sel.css(query)
        elif method == 're':
            return sel.re(query)
        else:
            raise ValueError('Please use correct method --> xpath,css,re')

    def extract_item(self, sels):
        '''
        提取内容，替换空格，内容用list返回
        '''
        contents = []
        for i in sels:
            content = re.sub(r'\s+', ' ', i.extract())
            if content != ' ':
                contents.append(content)
        return contents

    def extract_items(self, sel, rules, item, method):
        '''
        遍历至最小，提取内容，无内容返回空list
        '''
        for nk, nv in rules.items():
            if nk in ('__use'):
                continue

            # 判断关键字是否在item中
            if nk not in item:
                if type(item) == dict:
                    item[nk] = []
                else:
                    if nk in item.fields:
                        item[nk] = []
                    else:
                        continue

            nsel = self.item_selector(sel, nv, method)
            if nsel:
                # Without any extra spaces:
                item[nk].append(self.extract_item(nsel))
            else:
                item[nk].append([])

    # 1. item是一个单独的item，所有数据都聚合到其中 *merge
    # 2. 存在item列表，所有item归入items
    def traversal(self, sel, rules, item, method):
        '''
        深度优先遍历，最小子节点用__use字段标识，得到元素后加入items数组
        '''
        # print 'traversal:', sel, rules.keys()
        if '__use' in rules:

            self.extract_items(sel, rules, item, method)

        else:
            for nk, nv in rules.items():
                for i in self.item_selector(sel, nk, method):
                    self.traversal(i, nv, item, method)

    DEBUG = True

    def debug(self, sth):
        if self.DEBUG:
            print(sth)

    keywords = set(['__use'])

    def dfs(self, sel, rules, item, method):
        '''
        遍历
        '''
        if sel is None:
            return []
        self.traversal(
            sel, rules, item, method
        )
        return item

    def parse_with_rules(self, response, rules, item_class):
        item = item_class()
        for method, rule in rules.items():
            self.dfs(
                Selector(response),
                rules=rule,
                item=item,
                method=method,
            )
        return item

    ''' # use parse_with_rules example:
    def parse_people_with_rules(self, response):
        item = self.parse_with_rules(response, self.item_extractor, ZhihuPeopleItem)
        item['id'] = urlparse(response.url).path.split('/')[-1]
        info('Parsed '+response.url) # +' to '+str(item))
        return item
    '''
