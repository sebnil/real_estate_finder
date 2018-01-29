from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from database import RealEstate
import googlemaps
from realestate import shortcuts
from datetime import datetime, timedelta, time
import re
from dateutil import parser

def crawl(start_page):
    page_number = 1

    for page_number in range(1, 30):
        print('loop {}'.format(page_number))

        l = re.findall('(.*)(list-\d)(.*)', start_page)
        current_page = l[0][0] + 'list-' + str(page_number) + l[0][2]

        print('current_page {}'.format(current_page))
        links_to_real_estates = find_links_to_real_estates(current_page)
        insert_or_update_real_estate_item(links_to_real_estates)

        if len(links_to_real_estates) == 0:
            print('done.')
            break

def update_all_real_estates_in_database():
    estates = RealEstate.select()

    for estate in estates:
        estate_d = shortcuts.model_to_dict(estate)
        try:
            update_information_about_real_estate(estate_d['link'])
        except:
            print('error updating {}'.format(estate_d['link']))

def find_links_to_real_estates(link):
    found_links = []

    driver = get_chrome_driver_without_loading_images()

    try:
        driver.get(link)
        result_table = driver.find_element_by_id("searchResultsTbl")
        all_results = result_table.find_elements_by_class_name("resultBody")
        for one_result in all_results:
            address = one_result.find_element_by_css_selector("h2.rui-truncate a")
            link = address.get_attribute('href')
            found_links.append({'link': link})
    except:
        print('no results found')
    driver.close()

    return found_links

def update_information_about_real_estate(link):
    print('update_information_about_real_estate: {}'.format(link))
    item = {'link': link}
    driver = get_chrome_driver_without_loading_images()

    driver.get(link)
    item['location'] = driver.find_element_by_css_selector("h3.address").text
    item['price_per_week'] = get_price_per_week(driver.find_element_by_css_selector("p.priceText").text)
    item['bedrooms'] = get_bedrooms(driver.find_element_by_css_selector(".featureList").text)
    item['bathrooms'] = get_bathrooms(driver.find_element_by_css_selector(".featureList").text)
    item['date_available'] = get_date_available(driver)
    item['time_to_work'] = get_time_to_work(item['location'])
    item['time_from_work'] = get_time_from_work(item['location'])
    item['time_to_surfers_with_transit'] = get_time_to_surfers_with_transit(item['location'])
    item['time_to_surfers_by_car'] = get_time_to_surfers_by_car(item['location'])

    insert_or_update_real_estate_item(item)

    driver.close()

    return item


def get_chrome_driver_without_loading_images():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    return driver

def get_time_between_a_and_b(from_address, to_address, arrival_time, mode='driving'):
    gmaps = googlemaps.Client(key='AIzaSyDeSZYfgu3ksBn9-3By5b_kqIPsnW6hR7k')

    from_address = clean_adress_before_search(from_address)
    to_address = clean_adress_before_search(to_address)

    try:
        directions_result = gmaps.directions(from_address,
                                             to_address,
                                             mode=mode,
                                             arrival_time=arrival_time)
        a = directions_result[0]['legs'][0]['duration']['value']
        t = timedelta(seconds=a)
        ti = time(hour=t.seconds // 3600, minute=t.seconds // 60, second=t.seconds%60)
    except:
        return None
    return ti

def clean_adress_before_search(s):
    s = s.replace("'", "").replace('"', '').replace(' address available on request', ', Gold Coast')
    return s

def get_next_monday(time_of_day):

    now = datetime.now()
    next_monday = datetime(now.year, now.month, now.day, time_of_day.hour, time_of_day.minute, time_of_day.second)
    while next_monday.weekday() != 0:  # 0 for monday
        next_monday += timedelta(days=1)
    return next_monday

def get_time_to_work(address):
    return get_time_between_a_and_b(address, "76-84 Waterway Drive, Coomera, Australia", get_next_monday(time(7, 30, 0)))

def get_time_from_work(address):
    return get_time_between_a_and_b("76-84 Waterway Drive, Coomera, Australia", address, get_next_monday(time(16, 30, 0)))

def get_time_to_surfers_with_transit(address):
    surfers = 'Paradise Centre, Cavill Avenue, Surfers Paradise Queensland'
    return get_time_between_a_and_b(address, surfers, get_next_monday(time(16, 30, 0)), mode='transit')

def get_time_to_surfers_by_car(address):
    surfers = 'Paradise Centre, Cavill Avenue, Surfers Paradise Queensland'
    return get_time_between_a_and_b(address, surfers, get_next_monday(time(16, 30, 0)))

def insert_or_update_real_estate_item(items):
    if isinstance(items, dict):
        items = [items,]

    for item in items:
        estate, created = RealEstate.get_or_create(
            link=item['link'],
        )

        for key, value in item.iteritems():
            if key == 'link':
                continue

            setattr(estate, key, value)

        estate.save()


def get_price_per_week(s):
    try:
        f = re.findall('([\d|\.]*)( )', s)
        return int(f[0][0])
    except:
        try:
            f = re.findall('(\d*)', s)
            if '$' in s:
                return int(f[1])
            else:
                return int(f[0])
        except:
            print('error finding week price in {}'.format(s))
            return None


def get_bedrooms(s):
    try:
        f = re.findall('(Bedrooms:)(\d)', s)
        return int(f[0][1])
    except:
        return None

def get_bathrooms(s):
    try:
        f = re.findall('(Bathrooms:)(\d)', s)
        return int(f[0][1])
    except:
        return None

def get_date_available(driver):
    datestring = driver.find_element_by_css_selector(".available_date span").text
    if 'Available Now' in datestring:
        return 'Available Now'
    else:
        dt = parser.parse(datestring)
        d = datetime.date(dt)
        return d
