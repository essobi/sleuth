import scrapy
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from sleuth_crawler.scraper.scraper.items import ScrapyGenericPage

class UbcBroadCrawler(CrawlSpider):
    """
    Spider that crawls generically starting at UBC's homepage
    """
    name = "ubc_broad"

    start_urls = ["http://www.ubc.ca"]
    allowed = ['ubc', 'universityofbc']
    rules = (
        Rule(
            LinkExtractor(
                allow=('ubc', 'universityofbc', ), 
                deny=('youtube', 'twitter', 'facebook')
            ),
            callback='parse_item'
        ),
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.SolrPipeline': 400,
            'scraper.pipelines.JsonLogPipeline': 300,
        }
    }

    def parse_item(self, response):
        """
        Scrape page
        """
        output = ScrapyGenericPage()
        output['url'] = response.url
        # TODO: improve garbage removal
        output['raw_content'] = re.sub(r'<[^>]*?>', '', str(response.body))
        return output