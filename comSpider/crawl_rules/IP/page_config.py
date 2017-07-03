from crawl_rules.IP.items import IP

from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

# 设置爬虫名称
spider_name = "IP"

# 设置起始链接
start_urls = [
    "http://47.91.140.136:20001/ip",
]

domains = []
# 设置规则


# 提取器 link_extractor 其中 key 为 'xpath','css','re'中的一种或多种，value为相对应的解析路径

item_extractor = {

    'json': {
        '""':
            {
                '__use': 'dump',
                'mp_ip': '"mp_ip",',
                'mp_create_time': "'mp_create_time',",
                'mp_status':"'mp_status',",
                'mp_id':"'mp_id',",
                'mp_protocol':"'mp_protocol',",
            },
    },
}


crawl_item = IP

# 保存返回值，供测试使用
file_for_test = r'D:\scrapy-for-work\comSpider\crawl_rules\IP\list_page_item_return.json'
