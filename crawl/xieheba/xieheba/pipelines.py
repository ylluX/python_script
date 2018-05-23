# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class XiehebaPipeline(object):

    def __init__(self):
        self.f = open("static-xieheba.json", "w")
        self.mf = open("static-xieheba.md", "w")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(line)

        self.mf.write("[{}]({})\n".format(item['name'], item['url']))

        return item

    def close_spider(self):
        self.f.close()
        self.mf.close()