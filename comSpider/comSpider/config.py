from comSpider.items import AmazonItem

from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

# 设置爬虫名称
spider_name = "amazon-detail"

# 设置起始链接
start_urls = [
    "file:///D:/HTML/detail-page.htm",
    "file:///D:/HTML/detail-page2.htm",
    "file:///D:/HTML/detail-page3.htm",
]

domains = []
# 设置规则


# 提取器 css_extractor,xpath_extractor,process_extractor 分别对应

item_extractor = {
    'css': {
        '#centerCol': {
            '__use': 'dump',
            'title': '#productTitle::text',
            'star': '#acrPopover::attr(title)',
            'price': '#priceblock_ourprice::text',
        },
    },
    'xpath': {
        '//div[@id="centerCol"]': {
            '__use': 'dump',
            'title': './/span[@id="productTitle"]/text()',
            'star': './/span[@id="acrPopover"]/@title',
            'price': './/span[@id="priceblock_ourprice"]/text()',
        },
    }
}


crawl_item = AmazonItem
