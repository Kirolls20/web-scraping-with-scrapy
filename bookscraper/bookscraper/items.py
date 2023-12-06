# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    title = scrapy.Field()
    book_type = scrapy.Field()
    image_url = scrapy.Field()
    stars = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    
