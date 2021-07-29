import os
import scrapy


class MonstieSpider(scrapy.Spider):
    name = "monstiedb"
    if os.path.exists("results/monsties.json"):
            os.remove("results/monsties.json")
            print("Previous file deleted.")

    allowed_domains = ["kiranico.com"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results/monsties.json',
        'ITEM_PIPELINES': {'scrape.pipelines.RawDataPipeline': 300},
    }

    @classmethod
    def start_requests(self):
        url = "https://mhst.kiranico.com/mhs2/data/monsties"
        yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def parse(self, response):
        # retrieves row for each monstie in table
        monsties = response.xpath("//div[@class='card-body']/table/tbody/tr")

        # for loop to iterate through each row
        for monstie in monsties:
            # initialize dict
            data = {}

            # basic data for each monstie, contained in first data cell
            data["id"] = monstie.css("img::attr(src)").extract_first().split("micons/micon")[1].split(".png")[0]
            data["name"] = monstie.xpath(".//td[1]/div[1]/text()").get()[1:]
            data["tendency"] = monstie.xpath(".//td[1]/small/div[1]/text()").get()
            data["kinship"] = monstie.xpath(".//td[1]/small/div[2]/text()").get()
            data["actions"] = [monstie.xpath(".//td[1]/small/div[3]/text()").get()]
            # check if monstie has second action
            if monstie.xpath(".//td[1]/small/div[4]/text()").get():
                data["actions"].append(monstie.xpath(".//td[1]/small/div[4]/text()").get())

            # 
            stats_table = monstie.xpath(".//td[3]/small/table")
            data["speed"] = stats_table.xpath(".//thead/tr[1]/th[1]/text()").get().split(" : ")[1]
            
            stats_values = stats_table.xpath(".//tr")
            for row in stats_values:
                level = row.xpath(".//td[1]/text()").get()

                # skips row if row does not display stat values (e.g. header rows)
                if (level):
                    key = "lv" + level
                    data[key] = {
                        "maxHp": row.xpath(".//td[2]/text()").get(),
                        "recovery": row.xpath(".//td[3]/text()").get(),
                        "attack": {
                            "nonElem": row.xpath(".//td[4]/text()").get(),
                            "fire": row.xpath(".//td[5]/text()").get(),
                            "water": row.xpath(".//td[6]/text()").get(),
                            "thunder": row.xpath(".//td[7]/text()").get(),
                            "ice": row.xpath(".//td[8]/text()").get(),
                            "dragon": row.xpath(".//td[9]/text()").get()
                        },
                        "defense": {
                            "nonElem": row.xpath(".//td[10]/text()").get(),
                            "fire": row.xpath(".//td[11]/text()").get(),
                            "water": row.xpath(".//td[12]/text()").get(),
                            "thunder": row.xpath(".//td[13]/text()").get(),
                            "ice": row.xpath(".//td[14]/text()").get(),
                            "dragon": row.xpath(".//td[15]/text()").get()
                        }
                    }
                else:
                    continue
            
            yield data
