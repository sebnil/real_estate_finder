import unittest
from realestate import crawler, xlsx_generator
from datetime import time, datetime, timedelta


class MyTestCase(unittest.TestCase):

    def test_something(self):
        crawler.crawl()

    def test_insert_or_update(self):
        items = [{
            'link': 'https://www.realestate.com.au/property-unit-qld-broadbeach-422974878'
        }]
        crawler.insert_or_update_real_estate_item(items)

        items = [{
            'link': 'https://www.realestate.com.au/property-unit-qld-broadbeach-422974878',
            'price_per_week': '123',
            'time_to_work': time(0, 23, 0)

        }]
        crawler.insert_or_update_real_estate_item(items)

    def test_crawl_first_page(self):
        start_page = 'https://www.realestate.com.au/rent/property-unit+apartment-with-1-bedroom-between-400-700-in-gold+coast%2c+qld/list-1?maxBeds=1&source=location-search'
        crawler.crawl(start_page)

    def test_update_all_real_estates_in_database(self):
        crawler.update_all_real_estates_in_database()

    def test_xlsx_generator_generate(self):
        xlsx_generator.generate()


    def test_total_crawl(self):
        crawler.total_crawl()


    def test_find_links_to_real_estates(self):
        links = crawler.find_links_to_real_estates('https://www.realestate.com.au/rent/in-gold+coast,+qld/list-1')
        self.assertGreater(len(links), 0)

        no_links_found = crawler.find_links_to_real_estates('https://www.realestate.com.au/rent/in-gold+coast,+qld/list-1000')
        self.assertEqual(len(no_links_found), 0)

    def test_get_information_about_real_estate(self):
        item = crawler.update_information_about_real_estate('https://www.realestate.com.au/property-unit-qld-palm+beach-422972482')
        print(item)
        self.assertIsNotNone(item['location'])
        self.assertIsNotNone(item['bedrooms'])
        self.assertIsNotNone(item['date_available'])


    def test_delete_all_realestates(self):
        crawler.delete_all_realestates()

    def test_get_information_about_real_estate_2(self):
        item = crawler.update_information_about_real_estate('https://www.realestate.com.au/property-apartment-qld-palm+beach-422896098')
        print(item)
        self.assertIsNotNone(item['location'])


    def test_get_time_to_and_from_work(self):
        address = '701/40 Surf Parade"Travel Inn" Broadbeach'
        td = crawler.get_time_to_work(address)
        print(td)

        td = crawler.get_time_from_work(address)
        print(td)

    def test_tricky_address(self):
        tricky_address = 'Broadbeach address available on request'
        td = crawler.get_time_from_work(tricky_address)
        print(td)

    def test_time_to_surfers(self):
        address = "'LIBERTY PANORAMA' 1 Lennie Avenue Main Beach"
        td = crawler.get_time_to_surfers_with_transit(address)
        print(td)

    def test_get_next_monday(self):
        a = crawler.get_next_monday(time(7, 30, 0))
        print(a)

        a = crawler.get_next_monday(time(16, 0, 0))
        print(a)

    def test_get_price_per_week(self):
        s = '$460 per week'
        p = crawler.get_price_per_week(s)
        self.assertEqual(p, 460)

        s = '$470'
        p = crawler.get_price_per_week(s)
        self.assertEqual(p, 470)

        s = '$650.00 per week'
        p = crawler.get_price_per_week(s)
        self.assertEqual(p, 650)

        s = '420.00'
        p = crawler.get_price_per_week(s)
        self.assertEqual(p, 420)

    def test_parse_date(self):
        from dateutil import parser
        dt = parser.parse("Aug 28 1999 12:00AM")
        print(dt)

        dt = parser.parse("Fri 09-Feb-18")
        d = datetime.date(dt)
        print(dt)
        print(d)

if __name__ == '__main__':
    unittest.main()
