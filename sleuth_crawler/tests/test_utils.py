from django.test import TestCase
from scrapy.selector import Selector
import sleuth_crawler.scraper.scraper.spiders.parsers.utils as utils
import re

class TestUtils(TestCase):
    """
    Test parser utils
    parsers.utils
    """

    def test_strip_content(self):
        """
        Test webpage content stripping
        """
        data1 = "<h1>I am a typical HTML bracket</h1>"
        self.assertEqual(
            utils.strip_content(data1), ["I am a typical HTML bracket"]
        )
        data2 = "<body><p>blabla</p></body><property=''/><script>{def sadfljkasdf}</script>"
        self.assertEqual(
            utils.strip_content(data2), ["blabla"]
        )
        data_split_lines = "<body> line1 \n line2 \n line3 \n \n line4 </body>"
        self.assertEqual(
            utils.strip_content(data_split_lines), ["line1", "line2", "line3", "line4"]
        )
        data_invalid = {}
        self.assertEqual(
            utils.strip_content(data_invalid), [""]
        )

    def test_extract_element(self):
        """
        Test safe list extraction with default value ""
        """
        plist = [
            Selector(text="el1"),
            Selector(text="el2"),
            Selector(text="el3"),
        ]
        self.assertTrue(utils.extract_element(plist, 0))
        self.assertTrue(utils.extract_element(plist, 2))
        self.assertEqual(utils.extract_element(plist, 5), "")
