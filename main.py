import scrapy

from scrapy.crawler import CrawlerProcess

from spiders.spiders import KvantSpider as KvantSpider
from spiders.spiders import KvantikSpider as KvantikSpider


if __name__ == '__main__':
  process = CrawlerProcess()

  process.crawl(KvantSpider)
  process.crawl(KvantikSpider)

  process.start()