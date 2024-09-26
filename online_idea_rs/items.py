# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnlineIdeaRsItemCoffee(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    product_type = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    mrp = scrapy.Field()
    country = scrapy.Field()
    size = scrapy.Field()
