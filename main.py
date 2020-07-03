import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.spiders import KvantSpider as KvantSpider
from spiders.spiders import KvantikSpider as KvantikSpider


if __name__ == '__main__':
  process = CrawlerProcess(get_project_settings())

  process.crawl(KvantSpider)
  process.crawl(KvantikSpider)

  process.start()