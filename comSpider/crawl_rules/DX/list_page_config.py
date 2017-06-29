from crawl_rules.DX.items import DXListItem

from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

# 设置爬虫名称
spider_name = "DX-list"

# 设置起始链接
start_urls = [
    "file:///D:/scrapy-for-work/comSpider/test-HTML/DX-list-page.htm",
    "file:///D:/scrapy-for-work/comSpider/test-HTML/DX-list-page1.html",
]

domains = []
# 设置规则


# 提取器 link_extractor 其中 key 为 'xpath','css','re'中的一种或多种，value为相对应的解析路径

item_extractor = {

    'xpath': {
        '//ul[contains(@class,"productList")]/li':
            {
                '__use': 'dump',
                'img': './/div[@class="photo"]//img/@data-src',
                'title': './/div[@class="pi"]/p[@class="title"]//a/text()',
                'price': './/div[@class="pi"]/p[@class="price"]/text()',
                'sku': './/div[@class="po"]/p[@class="sku"]/text()',
            },
    },
}


crawl_item = DXListItem

# 保存返回值，供测试使用
file_for_test = r'D:\scrapy-for-work\comSpider\crawl_rules\DX\list_page_item_return.json'
