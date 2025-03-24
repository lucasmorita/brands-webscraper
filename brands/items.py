# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BrandsItem(Item):
    brand = Field()
    website = Field()
    gbin = Field()
    rtb_score = Field()
    country_of_origin = Field()
    industry = Field()
