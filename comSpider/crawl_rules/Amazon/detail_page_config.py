try:
    from crawl_rules.Amazon.items import AmazonItem
except:
    from items import AmazonItem
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


# 提取器 link_extractor 其中 key 为 'xpath','css','re'中的一种或多种，value为相对应的解析路径


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
