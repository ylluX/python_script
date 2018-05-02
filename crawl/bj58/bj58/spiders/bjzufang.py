# -*- coding: utf-8 -*-
import re
import scrapy

from bj58.items import Bj58Item


class BeijingchuzuSpider(scrapy.Spider):
    name = 'beijingchuzu'
    #allowed_domains = ['bj.58.com']
    start_urls = ['http://bj.58.com/chuzu/']

    def parse(self, response):
        node_list = response.xpath("//ul[@class='listUl']/li/div[@class='des']/h2/a")

        for node in node_list:
    	    name = node.xpath("./text()")[0].extract().strip().encode("utf-8")
    	    url = node.xpath("./@href")[0].extract().encode("utf-8")
    	    if name:
    	        yield scrapy.Request(url, callback=self.item_parse)

        next_url = response.xpath("//div[@class='pager']/a[@class='next']/@href").extract()
        if next_url:
            yield scrapy.Request(next_url[0], callback=self.parse)

    def item_parse(self, response):
    	item = Bj58Item()

    	money = response.xpath("//b[@class='f36']/text()").extract()
    	pay_type = response.xpath("//span[@class='c_333']/text()").extract()
    	rent_type = response.xpath(u"//li[span='租赁方式：']/span[2]/text()").extract()
    	house_type = response.xpath(u"//li[span='房屋类型：']/span[2]/text()").extract()
    	orient_floor = response.xpath(u"//li[span='朝向楼层：']/span[2]/text()").extract()
    	community = response.xpath(u"//li[span='所在小区：']/span[2]/a/text()").extract()
    	region = response.xpath(u"//li[span='所属区域：']/span[2]/a/text()").extract()
    	addr = response.xpath(u"//li[span='详细地址：']/span[2]/text()").extract()
    	phone = response.xpath("//span[@class='house-chat-txt']/text()").extract()
        location = response.xpath("//div[@class='view-more-detailmap view-more']/a/@href").extract()

        item["money"] = money[0].encode("utf-8") if money else ""
        item["pay_type"] = pay_type[0].encode("utf-8") if pay_type else ""
        item["rent_type"] = rent_type[0].encode("utf-8") if rent_type else ""
        item["house_type"] = house_type[0].encode("utf-8") if house_type else ""
        item["orient_floor"] = orient_floor[0].encode("utf-8") if orient_floor else ""
        item["community"] = community[0].encode("utf-8") if community else ""
        item["region"] = " ".join(region).encode("utf-8") if region else ""
        item["addr"] = addr[0].encode("utf-8") if addr else ""
        item["phone"] = phone[0].encode("utf-8") if phone else ""
        item["location"] = scrapy.utils.url.url_query_parameter(location[0].encode("utf-8"), "location") if location else ""

        for k, v in item.items():
        	item[k] = re.sub(r"\s+", " ", v)

    	yield item


