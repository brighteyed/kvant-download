import re
import scrapy

from typing import Iterator, Union

from spiders.items import Issue


class KvantSpider(scrapy.Spider):
    name = "kvant"

    custom_settings = {
        "ITEM_PIPELINES": {"spiders.pipelines.IssuePipeline": 300},
        "FEEDS": {"kvant.json": {"format": "json"}},
    }

    def start_requests(self) -> Iterator[scrapy.http.Request]:
        """Entry point"""

        archive_urls = ["http://kvant.mccme.ru/oblozhka_djvu.htm"] + [
            f"http://kvant.mccme.ru/oblozhka_djvu{n}.htm" for n in range(1, 7)
        ]
        for url in archive_urls:
            yield scrapy.Request(url=url, callback=self.parse_archive)

        yield scrapy.Request(url="http://kvant.mccme.ru/", callback=self.parse_main)

    def parse_main(
        self, response: scrapy.http.Response
    ) -> Union[Iterator[Issue], scrapy.http.Request]:
        links = (
            response.css("font.hdr b")[-1]
            .xpath("../../../../../../*")[-1]
            .xpath('.//td[@valign="top"]')
            .xpath(".//a[not(@hidden)][@href]")
        )
        for link in links:
            href = link.attrib["href"]
            if href.endswith(".pdf") or href.endswith(".djvu"):
                yield Issue(file=response.urljoin(href), text=link.css("::text").get())
            else:
                yield response.follow(url=href, callback=self.parse_page)

    def parse_archive(self, response: scrapy.http.Response) -> Iterator[Issue]:
        links = response.css("div a")
        for link in links:
            href = link.attrib["href"]
            if href.endswith(".djvu"):
                item = Issue(file=response.urljoin(href))

                img = link.css("img")
                if len(img) != 0:
                    item["cover"] = response.urljoin(img.attrib["src"])

                yield item

    def parse_page(self, response: scrapy.http.Response) -> Iterator[Issue]:
        pattern = re.compile(r".*\-b\.pdf")
        links = response.xpath("//a[@href]")
        for link in links:
            if re.match(pattern, link.attrib["href"]):
                item = Issue(
                    cover=response.urljoin(
                        link.xpath("./../../..").xpath(".//img").attrib["src"]
                    ),
                    file=response.urljoin(link.attrib["href"]),
                )

                text = response.css("h2::text").get()
                if text:
                    item["text"] = text

                yield item
