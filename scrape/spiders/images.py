import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrape.items import ImageItem


class MHImageSpider(CrawlSpider):
    name = "mhimage"
    allowed_domains = ["kiranico.com"]
    custom_settings = {
        'ITEM_PIPELINES': {'scrape.pipelines.ImgPipeline': 300},
    }

    def start_requests(self):
        url = "https://mhst.kiranico.com/mhs2/data/monsters"
        yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def parse(self, response):
        # Initialize dictionary
        items = []
        for row in response.xpath("//div[@class='card-body']/table/tbody/tr"):
            item = ImageItem()
            item['image_urls'] = self.url_join(row.css("img::attr(src)").extract(), response)

            item['image_name'] = row.css("img::attr(src)").extract_first().split("micons/micon")[1].split(".png")[0]

            items.append(item)

        return items

    def url_join(urls, response):
        joined_urls = []
        for url in urls:
            joined_urls.append(response.urljoin(url))
        return joined_urls

