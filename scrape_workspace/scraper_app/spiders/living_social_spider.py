from scrapy.spider import BaseSpider
from scrapy.selector import HtmlPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from scraper_app.items import LivingSocialDeal

class LivingSocialSpider(BaseSpider):
    """
    Spider for reggularly updated livingsocial.com site, 
    San Francisco Page
    """
    name = "livingsocial"
    allowed_domains = ["livingsocial.com"]
    start_urls = ["http://www.livingsocial.com/cities/15-san-fancisco"]

    deals_list_xpath = '//li[@dealid]'
    item_fields = {
        'title': './/spac[@itemscope]/meta[@itemprop="name"]-/@content',
        'link': './/a/@href',
        'location': './/a/@href',
        'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
        'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
    }
    
    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        Testing contracts:
        @url http://www.livingsocial.com/cities/15-san-francisco
        @returns items 1
        @scrapes title link

        """
        selector = HtmlXPathSelector(response)

        # iterate over deals
        for deal in selector.select(self.deals_list_xpath):
            loader = XPathItemLoader(LivingSocialDeal(), selector=deal)

            # define processors
            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

        # iterate over fields and add xpaths to the loader
        for field, xpath in self.item_fields.iteritems():
            loader.add_xpath(field, xpath)
        yield loader.load_item()
