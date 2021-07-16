from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from spiders.monsties import MonstieSpider
from spiders.genes import GeneSpider
from spiders.passive import PassiveSpider

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(MonstieSpider)
    yield runner.crawl(GeneSpider)
    yield runner.crawl(PassiveSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
