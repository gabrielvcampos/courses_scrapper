# -*- coding: utf-8 -*-
import scrapy
from courses.items import CoursesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from courses.helpers import trim_html

class VeducaSpider(scrapy.Spider):
    name = 'veduca'
    start_urls = ['https://veduca.org/p/cursos']

    def parse(self, response):
        courses = response.xpath('//section[contains(@class, "meus-cursos-show")]/div/div/a')
        for course in courses:
            yield scrapy.Request(
                url="https://veduca.org%s" % course.xpath('./@href').extract_first(),
                callback=self.parse_detail
            )


    def parse_detail(self, response):
        loader = ItemLoader(CoursesItem(), response=response)
        loader.default_output_processor = TakeFirst()
        loader.default_input_processor = MapCompose(trim_html)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//div[contains(@class, "titulo_banner_home")]/h1/text()')
        loader.add_xpath('headline', '//div[contains(@class, "titulo_banner_home")]/h3/text()')
        loader.add_xpath('instructors', '//div[contains(@class, "historia_ministrante-com-2")]/h2/text()')
        loader.add_xpath('lectures', '//section[contains(@class, "grade_curso")]//div[contains(@class, "card-body")]/i[contains(@class, "fa-play-circle")]/parent::div/text()')
        yield loader.load_item()