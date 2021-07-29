# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request

class ImgPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_name': item["image_name"]})
                for x in item.get('image_urls', [])]

    def item_completed(self, results, item, info):
        item['images'] = [x for ok, x in results if ok]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return '%s.png' % request.meta['image_name']


class RawDataPipeline(object):
    def process_item(self, item, spider):
        return item
