import unittest
from realestate import crawler
from datetime import time, datetime, timedelta

class MyTestCase(unittest.TestCase):

    def test_something(self):
        crawler.crawl()

    def test_insert_or_update(self):
        items = [{
            'link': 'https://www.realestate.com.au/property-unit-qld-broadbeach-422974878'
        }]
        crawler.insert_or_update_real_estate_item(items)

    def test_crawl_first_page(self):
        start_page = 'https://www.realestate.com.au/rent/in-gold+coast,+qld/'
        crawler.crawl(start_page)

    def test_find_links_to_real_estates(self):
        links = crawler.find_links_to_real_estates('https://www.realestate.com.au/rent/in-gold+coast,+qld/list-1')
        self.assertGreater(len(links), 0)

        no_links_found = crawler.find_links_to_real_estates('https://www.realestate.com.au/rent/in-gold+coast,+qld/list-1000')
        self.assertEqual(len(no_links_found), 0)

    def test_get_information_about_real_estate(self):
        item = crawler.update_information_about_real_estate('https://www.realestate.com.au/property-unit-qld-palm+beach-422972482')
        print(item)
        self.assertIsNotNone(item['address'])

    def test_get_time_to_and_from_work(self):
        address = '21/14 Jefferson Lane Palm Beach'
        td = crawler.get_time_to_work(address)
        print(td)

        td = crawler.get_time_from_work(address)
        print(td)

    def test_time_to_surfers(self):
        address = '21/14 Jefferson Lane Palm Beach'
        td = crawler.get_time_by_transit_to_surfers(address)
        print(td)

    def test_get_next_monday(self):
        a = crawler.get_next_monday(time(7, 30, 0))
        print(a)

        a = crawler.get_next_monday(time(16, 0, 0))
        print(a)


if __name__ == '__main__':
    unittest.main()
