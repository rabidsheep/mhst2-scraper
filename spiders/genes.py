import os
from xml.dom import minidom
from re import search

import scrapy

class GeneSpider(scrapy.Spider):
    name = "genedb"
    if (os.path.exists("results/genes.json")):
            os.remove("results/genes.json")
            print("Previous file deleted.")
    
    allowed_domains = ["kiranico.com"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results/genes.json',
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
            if (gene.xpath(".//td[3]/img/@title").getall()):
                data = {}
                name = gene.xpath(".//td[1]/div[1]/text()").get()
                
                # search name string to see if it has a size in parentheses (e.g. "(XL)")
                nameSplit = search("\(\w+\)", name)
                # if true, set size, otherwise size is null
                if (nameSplit):
                    data["name"] = name.split(" Gene ")[0]
                    data["size"] = name[name.find("(")+1:name.find(")")]
                else:
                    data["name"] = name.split(" Gene ")[0]
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
                temp = gene.xpath(".//td[3]/img[not(contains(@title, 'Palamute'))]/@title").getall()

                # only check for palamutes if temp array is not empty
                if temp:
                    palamutes = gene.xpath(".//td[3]/img[contains(@title, 'Palamute')]/@src").getall()

                    if palamutes:
                        i = 0

                        # loop through each palamute and assign element
                        while i < len(palamutes):
                            n = palamutes[i].split("micons/micon")[1]
                            n = n[0:n.find(".")]

                            # assign element based on icon number lol
                            if n == '168':
                                temp.append("Palamute (Fire)")
                            elif n == '167':
                                temp.append("Palamute (Water)")
                            elif n == '179':
                                temp.append("Palamute (Thunder)")
                            elif n == '169':
                                temp.append("Palamute (Non-Elemental)")
                            elif n == '178':
                                temp.append("Palamute (Ice)")
                            elif n == '177':
                                temp.append("Palamute (Dragon)")

                            i += 1

                # remove dupe monsties
                [data["monsties"].append(x) for x in temp if x not in data["monsties"]]
                
                yield (data)
            else:
                continue
