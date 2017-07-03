from crawl_rules.LT.items import LTListItem

from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

# 设置爬虫名称
spider_name = "LT-list"

# 设置起始链接
start_urls = [
    "file:///D:/scrapy-for-work/comSpider/test-HTML/LTlistpage.html",
]

domains = []
# 设置规则


# 提取器 link_extractor 其中 key 为 'xpath','css','re'中的一种或多种，value为相对应的解析路径

item_extractor = {

    'xpath': {
        '//div[contains(@class,"product-list")]//dl[@class="item-block"]':
            {
                '__use': 'dump',
                'img': './/dt//div[@class="img-box"]/img/@origin_src',
                'title': './dd[@class="prod-name"]//span/span/text()',
                'oldprice': './/p[@class="list-price"]/text()',
                'realprice': './/a[contains(@class,"price")]/text()',
                'favor': './/span[contains(@class,"favorite-for-cate")]/text()',
                'url': './dt/a/@href',
            },
    },
}


crawl_item = LTListItem

# 保存返回值，供测试使用
file_for_test = r'D:\scrapy-for-work\comSpider\crawl_rules\LT\list_page_item_return.json'
