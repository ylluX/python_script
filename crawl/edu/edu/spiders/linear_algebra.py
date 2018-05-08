# -*- coding: utf-8 -*-
import scrapy

from edu.items import EduItem

class LinearAlgebraSpider(scrapy.Spider):

    """
    爬去华夏大地教育网关于高等数学的网址
    """

    name = 'linear_algebra'

    allowed_domains = ['www2.edu-edu.com.cn']

    handle_httpstatus_list = [404]  # 设置scrapy不过滤404

    url = 'http://www2.edu-edu.com.cn/lesson_crs78/self/j_0022/soft/ch{:0>2}{:0>2}.html'

    u1 = 1
    u2 = 1
    u1_error = 0
    u2_error = 0
    u2_succeed = 0

    start_urls = [url.format(u1,u2)]

    def parse(self, response):

        item = EduItem()

        h1 = response.xpath("//h1/text()").extract()

        if response.status == 200:
            if h1:
                h1 = h1[0].encode("utf-8")
            else:
                h1 = ""
            item['h1'] = h1
            item['url'] = response.url

            self.u2_succeed += 1

            yield item

        else:

            # 如果u2连续三次错误，则u1加1，u2置0；
            # 如果u1连续三次错误，则退出程序

            self.u2_error += 1

            if self.u2_error > 3:
                self.u1 += 1
                self.u2 = 0
                self.u2_error = 0
                if self.u2_succeed == 0:
                    self.u1_error += 1
                self.u2_succeed = 0

            if self.u1_error > 3:
                return 

        self.u2 += 1

        yield scrapy.Request(self.url.format(self.u1, self.u2), callback=self.parse)
