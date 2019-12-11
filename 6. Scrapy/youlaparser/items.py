# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def price_cleaner(values):
    if values:
        values = int(values.replace('\u2009', ''))
        return values
    return values

def cleaner_photo(values):
    if values:
        values = values.replace('background-image:url(', '')
        values = values.replace(')', '')
        values = values.replace('/s/', '/l/')
        return values
    pass

class YoulaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_cleaner),output_processor = TakeFirst())
    production_year = scrapy.Field(output_processor=TakeFirst())
    total_milage = scrapy.Field(output_processor=TakeFirst())
    transmission = scrapy.Field(output_processor=TakeFirst())
    engine = scrapy.Field(output_processor=TakeFirst())
    engine_power = scrapy.Field(output_processor=TakeFirst())
    drive_type = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))

