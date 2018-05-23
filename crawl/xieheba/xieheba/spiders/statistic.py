# -*- coding: utf-8 -*-
import scrapy

from xieheba.items import XiehebaItem


class StatisticSpider(scrapy.Spider):
    name = "statistic"
    allowed_domains = ["https://mp.weixin.qq.com"]
    start_urls = ['https://mp.weixin.qq.com/s/9UQ-dXbP9wuOZ5B_TjDstg']

    def parse(self, response):
        a_list = response.xpath("//a")

        for a in a_list:
            item = XiehebaItem()
            name = a.xpath("text()").extract() or a.xpath("span/text()").extract()
            url = a.xpath("@href").extract()
            name = name[0].strip() if name else "XXXX"
            url = url[0] if url else "YYYY"
            if name not in ["协和八", "Reward", "留言", "取消", "打开"]:
                item["name"] = name
                item["url"] = url

                yield item
