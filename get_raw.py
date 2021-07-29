import os
import sys

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer

from scrape.spiders.monsties import MonstieSpider
from scrape.spiders.genes import GeneSpider
from scrape.spiders.passive import PassiveSpider

runner = CrawlerRunner()
configure_logging()

@defer.inlineCallbacks
def crawl():
    spiders = ['monsties', 'genes', 'passive']

    if len(sys.argv) < 2:
        print('\nNo valid spider names entered.\nAborting.')
        quit()
    else:
        invalid = []
        running = False
        i = 1
        while i <= len(sys.argv) - 1:
            if sys.argv[i] in spiders:
                i += 1
                continue
            else:
                invalid.append(sys.argv[i])
                i += 1

        if 'monsties' in sys.argv:
            running = True
            yield runner.crawl(MonstieSpider)
        if 'genes' in sys.argv:
            running = True
            yield runner.crawl(GeneSpider)
        if 'passive' in sys.argv:
            running = True
            yield runner.crawl(PassiveSpider)

        if running:
            reactor.stop()
        else:
            print("\nNo valid spider names entered.\nAborting.")
            os._exit(1)

        if len(invalid) > 0:
            print('\nInvalid spider name(s) found:' + str(invalid))


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
