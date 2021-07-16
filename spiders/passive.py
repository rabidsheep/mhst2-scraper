import os
from xml.dom import minidom
from re import search

import scrapy

class PassiveSpider(scrapy.Spider):
    name = "passivedb"
    if (os.path.exists("results/passive.json")):
            os.remove("results/passive.json")
            print("Previous file deleted.")
    
    allowed_domains = ["kiranico.com"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'results/passive.json',
    }

    @classmethod
    def start_requests(self):
        url = "https://mhst.kiranico.com/mhs2/data/skills"
        yield scrapy.Request(url=url, callback=self.parse)

    @classmethod
    def parse(self, response):
        skills = response.xpath("//div[@id='skillList']/div[@id='skill-0']/table/tr")

        for skill in skills:
            onActiveStatusId = skill.xpath(".//td[2]/small/div[1]/code/text()").get().split(":")[1]

            # ignore NPC-specific skills
            if onActiveStatusId == "150,202,169,0" or onActiveStatusId == "150,162,169,0":
                continue
            else:
                desc = skill.xpath(".//td[1]/div[2]/small/text()").get()

                # don't retrieve empty skills
                if desc:
                    data = {}
                    name = skill.xpath(".//td[1]/div[1]/text()").get()
                    data["name"] = name[1:len(name)-1]
                    data["main"] = desc
                    data["chance"] = "N/A"
                    data["default"] = "N/A"
                    data["upOne"] = "N/A"
                    data["upTwo"] = "N/A"
                    
                    if desc.find("(Chance)" ) > -1:
                        data["main"] = data["main"].split("(Chance)")[0]
                        data["chance"] = desc.split("(Chance)")[1].split("(Default)")[0].strip()
                    if desc.find("(Default)") > -1:
                        data["main"] = data["main"].split("(Default)")[0]
                        data["default"] = desc.split("(Default)")[1].split("(UP 1)")[0].strip()
                    if desc.find("(UP 1)") > -1:
                        data["upOne"] = desc.split("(UP 1)")[1].split("(UP 2)")[0].strip()
                    if desc.find("(UP 2)") > -1:
                        data["upTwo"] = desc.split("(UP 2)")[1].strip()
                        
                    data["main"] = data["main"].strip()
                    yield(data)
                else:
                    continue
