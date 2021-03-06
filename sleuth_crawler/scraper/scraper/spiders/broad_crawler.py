import scrapy
from sleuth_crawler.scraper.scraper.spiders.parsers import generic_page_parser, reddit_parser
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from sleuth_crawler.scraper.scraper.settings import PARENT_URLS

class BroadCrawler(CrawlSpider):
    '''
    Spider that broad crawls starting at list of predefined URLs
    '''
    name = 'broad_crawler'

    # These are the links that the crawler starts crawling at
    start_urls = PARENT_URLS

    # Rules for what links are followed are defined here
    allowed_terms = [r'(ubc)', r'(university)', r'(ubyssey)', r'(prof)', r'(student)', r'(faculty)']
    denied_terms = [r'(accounts\.google)', r'(intent)', r'(lang=)']
    GENERIC_LINK_EXTRACTOR = LinkExtractor(allow=allowed_terms, deny=denied_terms)

    rules = (
        Rule(
            GENERIC_LINK_EXTRACTOR,
            follow=True, process_request='process_request',
            callback='parse_generic_item'
        ),
    )

    # Specifies the pipeline that handles data returned from the parsers
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
        }
    }

    def process_request(self, req):
        '''
        Assigns best callback for each request
        '''
        if 'reddit.com' in req.url:
            req = req.replace(priority=100)
            if 'comments' in req.url:
                req = req.replace(callback=self.parse_reddit_post)
            else:
                req = req.replace(callback=self.no_parse)

        return req

    def parse_start_urls(self, resp):
        '''
        Parses the start_urls
        '''
        if 'reddit.com' in resp.url:
            return self.parse_reddit_post(resp)
        return self.parse_generic_item(resp)

    ###############
    ## CALLBACKS ##
    ###############

    def parse_generic_item(self, response):
        '''
        Points to generic_page_parser (the default parser for this crawler)
        '''
        links = self._get_links(response)
        return generic_page_parser.parse_generic_item(response, links)

    def parse_reddit_post(self, response):
        '''
        Points to reddit_parser.parse_comments
        '''
        links = self._get_links(response)
        return reddit_parser.parse_post(response, links)

    def no_parse(self, response):
        '''
        Visit page without parsing it - this allows the URLS of this page to
        be extracted and visited if there are any relevant links
        '''
        # TODO: does this work?
        return

    def _get_links(self, response):
        links = []
        for link in self.GENERIC_LINK_EXTRACTOR.extract_links(response):
            if link.url != response.url:
                links.append(link.url)
        return links
