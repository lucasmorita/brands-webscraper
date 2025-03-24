from pathlib import Path
from string import ascii_uppercase

import scrapy

from ..items import BrandsItem

BASE_URL = 'https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?nameFilter='
BASE_DIR = Path(__file__).resolve().parent.parent.name

class BrandsSpider(scrapy.Spider):
    name = 'brands'

    def start_requests(self):
        urls = [BASE_URL + l for l in ascii_uppercase]
        # urls = [BASE_URL+'A']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.xpath("//div[@class='brandLine']//a/@href").getall()

        for link in hrefs:
            absolute_url = response.urljoin(link) # important to make relative urls absolute.
            # self.log(absolute_url)
            yield scrapy.Request(url=absolute_url, callback=self.parse_brands)


    def parse_brands(self, response):
        brand_details = response.xpath("//div[@class='branddetails']")
        for detail in brand_details:
            brand = detail.xpath(".//div[@class='brandName']/span/text()").get()
            labels = detail.xpath(".//div[@class='brandInfoRow']/div[@class='brandInfoLabel']/span//text()").getall()
            values = detail.xpath(".//div[@class='brandInfoRow']/div[@class='brandInfoText']/span//text()").getall()
            item = BrandsItem()
            item['brand'] = brand.strip()
            for l, v in zip(labels, values):
                item[l.strip().lower().replace(' ', '_')] = v.strip()
            yield item