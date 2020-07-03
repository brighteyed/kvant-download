import scrapy

class Issue(scrapy.Item):
    file = scrapy.Field()
    text = scrapy.Field()
    cover = scrapy.Field()
    year = scrapy.Field()
    issue = scrapy.Field()
