import scrapy

from typing import Iterator

from spiders.items import Issue


class KvantikSpider(scrapy.Spider):
    name = "kvantik"
    allowed_domains = ["kvantik.com/archive"]
    start_urls = ["http://kvantik.com/archive/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "spiders.pipelines.IssuePipeline": 300,
            "spiders.pipelines.DropSamplesPipeline": 500,
        },
        "FEEDS": {"kvantik.json": {"format": "json"}},
    }

    def parse(self, response: scrapy.http.Response) -> Iterator[Issue]:
        for item in response.css("div.gallery"):
            yield Issue(
                cover=response.urljoin(item.css("a img::attr(src)").get()),
                file=response.urljoin(item.css("a::attr(href)").get()),
            )
