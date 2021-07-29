from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from scrape.spiders.images import MHImageSpider

configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(MHImageSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
