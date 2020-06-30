import scrapy

from spiders.items import Issue


class KvantikSpider(scrapy.Spider):
    name = 'kvantik'
    allowed_domains = ['kvantik.com/archive']
    start_urls = ['http://kvantik.com/archive/']

    def parse(self, response):
        for item in response.css('div.gallery'):
            yield Issue(cover=response.urljoin(item.css('a img::attr(src)').get()),
                file=response.urljoin(item.css('a::attr(href)').get()))
            
        
