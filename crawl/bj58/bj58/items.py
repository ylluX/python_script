# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Bj58Item(scrapy.Item):
    # define the fields for your item here like:
    money = scrapy.Field()
    pay_type = scrapy.Field()
    rent_type = scrapy.Field()
    house_type = scrapy.Field()
    orient_floor = scrapy.Field()
    community = scrapy.Field()
    region = scrapy.Field()
    addr = scrapy.Field()
    phone = scrapy.Field()
    location = scrapy.Field()
