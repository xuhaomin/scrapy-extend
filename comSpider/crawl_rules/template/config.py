try:
    from crawl_rules.template.items import Item
except:
    from items import Item
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

# 设置爬虫名称
spider_name = ""

# 设置起始链接
start_urls = [

]

domains = []
# 设置规则


# 提取器 link_extractor 其中 key 为 'xpath','css','re'中的一种或多种，value为相对应的解析路径


item_extractor = {
    'css': {

    },
    'xpath': {

    },
    're': {

    }
}


crawl_item = Item
