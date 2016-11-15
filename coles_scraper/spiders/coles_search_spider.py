import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
from lxml import html
logging.DEBUG
logging.basicConfig(level=logging.DEBUG)
# class DmozSpider(scrapy.Spider):
#     name = "coles_search"
#     allowed_domains = ["coles.com.au",
#                        "shop.coles.com.au"]
#     #base_url = 'https://www.shop.coles.com.au/'
#     #search_url = base_url+search_dir
#     # TODO: generate fresh base search url for capturing the
#     #       -- storeId=10601
#     #       -- catalogId=10567
#     search_url = lambda search_term: 'https://shop.coles.com.au/online/SearchDisplay?storeId=10601&catalogId=10576&searchTerm=%s' % search_term
#
#     items = [
#             "milk",
#             ]
#     start_urls = [search_url(item) for item in items]
#
#     for url in start_urls:
#         print "generated url: %s"  %url
#
#
#     def parse(self, response):
#         dict_parser = re.compile('\{|\,(?P<key>[A-z]+)\:\'(?P<item>.*)\'')
#         selector = scrapy.selector.Selector(response=response)
#         items_found = response.selector.xpath("//div/@data-social")
#         items_dict = {}
#         for item in items_found:
#             print item.extract()
#             parsed_dict = dict(re.findall(dict_parser, item.extract()))
#             print parsed_dict['title']
#             print parsed_dict['description']
#             print parsed_dict['productDisplayUrl']
#             items_dict[parsed_dict['title'].strip()] = {'description': parsed_dict['description'],
#                                                 'url': parsed_dict['productDisplayUrl']}



class ColesScraper(CrawlSpider):

    name = 'coles_search'
    allowed_domains = ["shop.coles.com.au"]

    search_url = lambda search_term: r"https://shop.coles.com.au/online/SearchDisplay?storeId=10601&catalogId=10576&searchTerm=%s" % search_term

    items = [
            "chocolate",
            ]
    start_urls = [search_url(item) for item in items]
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="next"]/a'),
            callback="parse_page", follow= True),
        # Rule(LinkExtractor(allow=(),
        #     restrict_xpaths=("//a[@title='Next page of results']",)),
        #     callback="parse_page", follow= True),
        # Rule(LinkExtractor(allow=(),
        #     restrict_xpaths=('//a[@class="btn-aqua action-change-page"]',)),
        #     callback="parse_page", follow= True),


            )



    def parse_page(self, response):
        items_dict = {}
        dict_parser = re.compile('\{|\,(?P<key>[A-z]+)\:\'(?P<item>.*)\'')
        selector = scrapy.selector.Selector(response=response)
        items_found = response.selector.xpath("//div/@data-social")
        for item in items_found:
            print item.extract()
            parsed_dict = dict(re.findall(dict_parser, item.extract()))
            print parsed_dict['title']
            print parsed_dict['description']
            print parsed_dict['productDisplayUrl']
            items_dict[parsed_dict['title'].strip()] = {'description': parsed_dict['description'],
                                                'url': parsed_dict['productDisplayUrl']}

        #print items_dict
        return items_dict
        print "AAA"
# import scrapy
# from scrapy.spiders import CrawlSpider, Rule

#
class Scrapy1Spider(CrawlSpider):
    name = "craiglist"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = (
        'http://sfbay.craigslist.org/search/npo',
    )

    rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_page", follow= True),)

    def parse_page(self, response):
        site = html.fromstring(response.body_as_unicode())
        titles = site.xpath('//div[@class="content"]/p[@class="row"]')
        print len(titles), 'AAAA'
