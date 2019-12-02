# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from youlaparser.items import YoulaparserItem
from scrapy.loader import ItemLoader

class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    start_urls = ['https://auto.youla.ru/moskva/cars/used/?bodyTypes%5B0%5D=6']

    def parse(self, response: HtmlResponse):
        next_page=response.xpath('//div[@class="Paginator_block__2XAPy app_roundedBlockWithShadow__1rh6w"]/a/@href').extract()
        yield response.follow(next_page[1], callback=self.parse)

        ads=response.xpath('//div[@id="serp"]/span/article/div/div/a/@href').extract()

        for link in ads:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader=ItemLoader(item=YoulaparserItem(),response=response)
        loader.add_xpath('title','//div[@class="AdvertCard_advertTitle__1S1Ak"]/text()')
        loader.add_xpath('price', '//div[@class="AdvertCard_priceBlock__1hOQW"]/div/text()')
        loader.add_xpath('production_year', '//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-year"]/a/text()')
        loader.add_xpath('total_milage', '//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-mileage"]/text()')
        loader.add_xpath('transmission', '//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-transmission"]/text()')
        loader.add_xpath('engine', '//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-engineInfo"]/text()')
        loader.add_xpath('engine_power', '//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-enginePower"]/text()')
        loader.add_xpath('drive_type', '//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-driveType"]/text()')
        loader.add_xpath('photos', '//button[contains(@class, "PhotoGallery_thumbnailItem__UmhLO")]/@style')
        yield loader.load_item()


        # title=response.xpath('//div[@class="AdvertCard_advertTitle__1S1Ak"]/text()').extract_first()
        # price=response.xpath('//div[@class="AdvertCard_priceBlock__1hOQW"]/div/text()').extract_first()
        # production_year=response.xpath('//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-year"]/a/text()').extract_first()
        # total_milage=response.xpath('//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-mileage"]/text()').extract_first()
        # transmission = response.xpath('//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-transmission"]/text()').extract_first()
        # engine = response.xpath('//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-engineInfo"]/text()').extract_first()
        # engine_power = response.xpath('//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-enginePower"]/text()').extract_first()
        # drive_type = response.xpath('//div[@class ="AdvertCard_specs__2FEHc"]/div/div/div[@data-target="advert-info-driveType"]/text()').extract_first()
        # photos=response.xpath('//button[contains(@class, "PhotoGallery_thumbnailItem__UmhLO")]/@style').extract()
        # yield YoulaparserItem(title=title,price=price,production_year=production_year,total_milage=total_milage, transmission=transmission, engine=engine, engine_power=engine_power, drive_type=drive_type, photos=photos)


