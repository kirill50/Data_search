# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page=response.xpath('//a[@rel="next"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div/div/div/div/div/div/div/div/div/div/div/div/a/@href').extract()

        for link in links:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name=response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/text()|//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/span[@class="_1rS-s"]/text()').extract_first()
        employer=response.xpath('//h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract_first()
        min_salary=response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/span/text()').extract_first()
        max_salary=response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/span[@x-path=1]/text()|//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/span[3]/text()').extract_first()
        currency=response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/span[4]/text()').extract_first()


        yield JobparserItem(name=name, min_salary=min_salary, max_salary=max_salary, currency=currency, employer=employer, link=response.url)




