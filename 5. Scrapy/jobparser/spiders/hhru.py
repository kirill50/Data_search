# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy_items = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacansy_items:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()|//h1[@data-qa="vacancy-title"]/span/text()').extract_first()
        employer = response.xpath('//a[@itemprop="hiringOrganization"]/span/span/text()|//a[@itemprop="hiringOrganization"]/span/text()').extract()
        min_salary = response.xpath('//span[@itemprop="value"]/meta[@itemprop="minValue"]/@content').extract()
        max_salary = response.xpath('//span[@itemprop="value"]/meta[@itemprop="maxValue"]/@content|//span[@itemprop="value"]/meta[@itemprop="value"]/@content').extract()
        currency=response.xpath('//span[@itemprop="baseSalary"]/meta[@itemprop="currency"]/@content').extract()

        yield JobparserItem(name=name, min_salary=min_salary, max_salary=max_salary, currency=currency, employer=employer, link=response.url)





