# -*- coding: utf-8 -*-
import scrapy


class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    category = None


    def start_requests(self):
        if self.category is None:
            yield scrapy.Request(
                url='https://www.coursera.org/browse/?language\=pt',
                    callback=self.parse
            )
        else:
            yield scrapy.Request(
                url= 'https://www.coursera.org/browse/%s' % self.category,
                callback=self.parse_category
            )


    def parse(self, response):
        categories = response.xpath('//a[contains(@data-click-key, "browse.browse.click.explore_domains_card")]/@href').extract()

        for cat in categories:
            self.log("Logando CATEGORIA %s" % cat)
            yield scrapy.Request(
                url='https://www.coursera.org%s' % cat,
                callback=self.parse_category
            )


    def parse_category(self, response):
        
        courses_link = response.xpath('//a[contains(@data-click-key, "browse.browse.click.collection_product_card")]/@href').extract()

        for link in courses_link:
            self.log("Logando CURSO %s" % link)
            yield scrapy.Request(
                url='https://www.coursera.org%s' % link,
                callback=self.parse_course
            )

    
    def parse_course(self, response):
        self.log(response.xpath('//title/text()').extract_first())
        yield {
            'title': response.xpath('//title/text()').extract_first()
        }