import os
import scrapy


class GeneSpider(scrapy.Spider):
    name = "genedb"
    if os.path.exists("results/genes.json"):
            os.remove("results/genes.json")
            print("Previous file deleted.")
    
    allowed_domains = ["kiranico.com"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results/genes.json',
        'ITEM_PIPELINES': {'scrape.pipelines.RawDataPipeline': 300},
    }

    @classmethod
    def start_requests(self):
        url = "https://mhst.kiranico.com/mhs2/data/genes"
        yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def parse(self, response):
        genes = response.xpath("//div[@class='card-body']/table/tbody/tr")

        for gene in genes:
            # only scrape row if gene has monsties linked to it
            if gene.xpath(".//td[3]/img/@title").getall():
                data = {}
                name = gene.xpath(".//td[1]/div[1]/text()").get()
                
                # search name string to see if it has a size in parentheses (e.g. "(XL)")
                data["name"] = name.split("(")[0].strip()

                if len(name.split(" (")) > 1:
                    data["size"] = name.split("(")[1].split(")")[0]
                else:
                    data["size"] = None

                data["type"] = gene.xpath(".//td[1]/small/div[1]/text()").get().split(" ")[0]
                data["element"] = gene.xpath(".//td[1]/small/div[2]/text()").get()
                data["level"] = gene.xpath(".//td[1]/small/div[3]/text()").get().split(" : ")[1]
                data["tier"] = gene.xpath(".//td[1]/small/div[4]/text()").get().split(" : ")[1]
                data["skill"] = {
                        "name": gene.xpath(".//td[2]/div[1]/text()").get(),
                        "desc": gene.xpath(".//td[2]/div/small/text()").get()
                    }
                data["monsties"] = []
                
                # temp array for all monsties that can carry a gene naturally
                temp = gene.css("img::attr(src)").extract()

                # remove dupe monsties
                [data["monsties"].append(x.split("micons/micon")[1].split(".png")[0])
                 for x in temp if x not in data["monsties"]]
                
                yield data
            else:
                continue