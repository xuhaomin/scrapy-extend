from crawl_rules.Amazon.items import AmazonListItem

from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

# 设置爬虫名称
spider_name = "amazon-list"

# 设置起始链接
start_urls = [
    "file:///D:/scrapy-for-work/comSpider/test-HTML/list-page.htm",
]

domains = []
# 设置规则


# 提取器 link_extractor 其中 key 为 'xpath','css','re'中的一种或多种，value为相对应的解析路径

item_extractor = {

    'xpath': {
        '//div[@id="search-results"]': {
            './/h2[@id="s-result-count"]': {
                '__use': 'dump',
                'num': './text()',
            },
            './/li[starts-with(@id,"result")]': {
                '__use': 'dump',
                'rank': './@id',
                'title': './div/div[3]//a/@title',
                'brand': './div/div[2]//span/text()',
                'price_currency': './div/div[3]//sup[@class="sx-price-currency"]/text()',
                'price_whole': './div/div[3]//span[@class="sx-price-whole"]/text()',
                'price_frac': './div/div[3]//sup[@class="sx-price-fractional"]/text()',
                'score': './div/div[3]//i[contains(@class,"a-icon-star")]/span/text()',
                'img': './div/div[1]//a/@href'

            },
        },

    },
}


crawl_item = AmazonListItem

# 保存返回值，供测试使用
file_for_test = r'D:\scrapy-for-work\comSpider\crawl_rules\Amazon\list_page_item_return.json'