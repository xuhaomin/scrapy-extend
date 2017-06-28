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




思想：
    基于css，xpath建立的dom树，item作为叶子节点进行采集 
    'xpath': （对应xpath方法）
        {
            xpath1: {
                xpath1-2: {
                    '__use':'dump',
                    'name':xpath1-2-1,
                    'sign':xpath1-2-2,
                    'location':xpath1-2-3,
                }, 
            }
        }
   're':（对应re方法）
        {
            '__use':'dump',
            itemX:regex1,
        }
    'css': （对应css方法）
        {
            css1: {
                css1-2: {
                    '__use':'dump',
                    item5:css1-2-1,
                    item6:css1-2-2,
                    item7:css1-2-3,
                }, 
            }
        }


接口返回值目前有两种方案：
方案一 返回包含多个item的list  例如 return [item1,item2,item3]
方案二 是返回单个item，其各字段的值是采集下来对应值的list   例如 return item = {key1:[v1,v2,v3],key2:[v1,v2,v3]}


方案一就是初始化一个list，然后遍历dom树，把所有叶子节点采集到的内容作为一个item加入list中
    那这样，如果item需要不同方法得到，如：
    'xpath': 
        {
            xpath1: {
                xpath1-2: {
                    '__use':'dump',
                    'name':xpath1-2-1,
                    }
                }
        }，
    're':
        {
            '__use':'dump',
            'sign':regex,
        }
    这样 name 和 sign 字段就得分别在不同item中返回  因为它们不在一个叶子节点下。


方案二就是在开始初始化一个item，遍历dom树，把所有叶子节点采集到的值，根据字段名对应的插入初始化建立的item中
    但是同样：
    'xpath': 
        {
            xpath1: {
                xpath1-2: {
                    '__use':'dump',
                    'name':xpath1-2-1,
                    }
                }
        }，
    're':
        {
            '__use':'dump',
            'sign':regex,
        }

    面对这样一个情况，如果name返回了10个值，sign返回了9个值，很难一一对应。


返回单个item如果遇到单个页面，例如列表页，需要返回多个item的情况会比较麻烦。  
    例如：出现某个值缺失，key1采了10个值 key2采了9个值，就比较难匹配，会发生冲突
    解决方法： 写xpath或者回调时，尽量让返回值数量匹配，或者将采集结果丢到item-pipeline进行处理。
返回多个item，面对需要多种（例如正则加xpath）方法取不同字段值的情况，比较麻烦，
    比如key1，key2通过正则取，key3通过xpath取，key4通过某函数取，不同方法产生的值就得写在不同item里（分属于不同叶子结点），后续处理起来比较麻烦，
    解决方法： 尽量只用一种方案取值（只用xpath选择器或者只用函数）

或者写两种spider：
    列表页的信息采集用返回多个item的spider
    详情页的信息采集用返回单个item的spider
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
            if nk not in item:
                item[nk] = []
            nsel = self.item_selector(sel, nv, method)
            if nsel:
                # item[nk] += [i.extract() for i in sel.item_selector(sel, nv, method)]
                # Without any extra spaces:
                item[nk] += self.extract_item(nsel)
            else:
                item[nk] = []

    # 1. item是一个单独的item，所有数据都聚合到其中 *merge
    # 2. 存在item列表，所有item归入items
    def traversal(self, sel, rules, item_class, item, items, method):
        '''
        深度优先遍历，最小子节点用__use字段标识，得到元素后加入items数组
        '''
        # print 'traversal:', sel, rules.keys()
        if item is None:
            item = item_class()
        if '__use' in rules:

            unique_item = item_class()
            self.extract_items(sel, rules, unique_item, method)
            items.append(unique_item)

        else:
            for nk, nv in rules.items():
                for i in self.item_selector(sel, nk, method):
                    self.traversal(i, nv, item_class, item, items, method)

    DEBUG = True

    def debug(self, sth):
        if self.DEBUG == True:
            print(sth)

    def deal_text(self, sel, item, k, v, method):
        if (v.endswith('::text') or v.endswith(r'text()')) and self.auto_join_text:
            item[k] = ' '.join(
                self.extract_item(
                    self.item_selector(sel, v, method)
                ))
        else:
            _items = self.extract_item(self.item_selector(sel, v, method))
            item[k] = _items

    keywords = set(['__use'])

    def traversal_dict(self, sel, rules, item_class, item, items, method):
        '''
        深度优先遍历，最小子节点用__use字段标识，得到元素后加入items数组
        '''
        # import pdb; pdb.set_trace()
        item = {}
        for k, v in rules.items():
            if type(v) != dict:
                if k in self.keywords:
                    continue
                if type(v) == list:
                    continue
                self.deal_text(sel, item, k, v, method)
                #import pdb;pdb.set_trace()
            else:
                item[k] = []
                for i in self.item_selector(sel, k, method):
                    #print(k, v)
                    self.traversal_dict(
                        i, v, item_class, item, item[k], method)
        items.append(item)

    def dfs(self, sel, rules, item_class, method):
        '''
        遍历，区分使用封装item和原生字典两种class
        '''
        if sel is None:
            return []

        items = []
        if item_class != dict:
            self.traversal(
                sel, rules, item_class, None, items, method
            )
        else:
            self.traversal_dict(
                sel, rules, item_class,
                None, items, method
            )

        return items

    def parse_with_rules(self, response, rules, item_class):
        items = []
        for method, rule in rules.items():
            item = self.dfs(
                Selector(response),
                rules=rule,
                item_class=item_class,
                method=method,
            )
            items += item
        return items

    ''' # use parse_with_rules example:
    def parse_people_with_rules(self, response):
        item = self.parse_with_rules(response, self.all_css_rules, ZhihuPeopleItem)
        item['id'] = urlparse(response.url).path.split('/')[-1]
        info('Parsed '+response.url) # +' to '+str(item))
        return item
    '''
