# -*- coding: utf-8 -*-
import scrapy


class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    start_urls = ['https://www.udacity.com/courses/all/']

    def parse(self, response):
        divs = response.xpath("/html/body/ir-root/ir-content/ir-course-catalog/section[3]/div/div[2]/ir-course-card-catalog/div/div/div/div")
        for div in divs:
            link = div.xpath('.//h3/a')
            href = link.xpath('./@href').extract_first()
            category = div.xpath('.//h4/text()').extract_first()
            yield scrapy.Request(
                url='https://www.udacity.com%s' % href,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        description = response.xpath('//div[contains(@class, "description")]/p/text()').extract_first()
        image = response.xpath('//img[contains(@class, "images")]/@src').extract_first()
        instructors = []
        for div in response.xpath('//ir-nd-instructors//div[contains(@class, "card")]'):
            instructors.append(
                {
                    'name': div.xpath('./h5/text()').extract_first(),
                    'job': div.xpath('./p[1]/text()').extract_first(),
                    'image': div.xpath('./img/@src').extract_first(),
                    'description': div.xpath('./p[2]/text()').extract_first()
                }
            )

        yield {
            'title': title,
            'description': description,
            'image': image,
            'instructor': instructors
        }
