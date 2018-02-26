#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import sys
import requests
from datetime import datetime
from CityEventClass import CityEvent
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

RED_COLOR_TAG = "\x1B[91;40m"
BOLD_TAG = "\x1B[1m"
CLOSE_TAG = "\x1B[0m"
XML_PATH = "http://bip.poznan.pl/api-xml/bip/news/-,c,8380/"
HINT_TEXT = BOLD_TAG + "usage: " + CLOSE_TAG + \
            "Type date in format YYYY-MM-DD" \
            " or street (at least 4 characters)>"
ERROR_TEXT = RED_COLOR_TAG + BOLD_TAG + "error: " + CLOSE_TAG


def xml_download(XML_PATH):
    # Download XML Element from PATH
    # Returns Element object or False if something goes wron

    print("Downloading xml file...")
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        r = s.get(XML_PATH)
    except requests.ConnectionError:
        print(ERROR_TEXT + "Check your internet connection")
        return False
    if r.status_code == 200:
        try:
            return ET.fromstring(r.content)
        except ET.ParseError:
            print(ERROR_TEXT +
                  "Wrong XML object, check your XML_PATH variable")
            return False
    else:
        print(ERROR_TEXT +
              "Something went wrong... http_status = " + str(r.status_code))


def xml_to_cityevents(element_object):
    # Read Element object trough and get data from:
    #   1. <nw_from_date>
    #   2. <nw_to_date>
    #   3. <nw_text>
    # Returns list of objects CityEvent

    city_events_list = []
    announcements_items = element_object.find("data") \
                                        .find("komunikaty_i_ogloszenia") \
                                        .find("items")

    for announcement in announcements_items:
        event_start_date = announcement.find("nw_from_date").text
        event_end_date = announcement.find("nw_to_date").text
        event_description = announcement.find("nw_text").text
        event_description = re.sub('<.*?>', '', str(event_description))
        city_events_list.append(CityEvent(event_start_date,
                                          event_end_date,
                                          event_description))

    return city_events_list


def search_events(city_events_list, event_date, event_desc_pattern):
    # Search trough list of CityEvent objects woth date or pattern(street)
    # Returns list of CityEvent objects.

    if event_desc_pattern is None and event_date is not None:
        return [x for x in city_events_list
                if x.date_search(event_date)]
    elif event_desc_pattern is not None and event_date is None:
        return [x for x in city_events_list
                if x.description_search(event_desc_pattern)]


def street_validator(street):

    if street is None or len(street) >= 4:
        return True
    else:
        return False


def date_validator(date):

    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False


def main():
    # Main function

    date = None
    street = None

    prog = re.compile('^[0-9]{4}.*')

    input_value = input('Type street or date <YYYY-MM-DD>: ')

    if prog.match(input_value) and date_validator(input_value) is False:
        print(HINT_TEXT)
        sys.exit()
    elif date_validator(input_value) is not False:
        date = date_validator(input_value)
    else:
        street = input_value

    if not street_validator(street):
        print(HINT_TEXT)
        sys.exit()

    xml_element = xml_download(XML_PATH)
    if xml_element is False:
        sys.exit()
    else:
        lista = search_events(xml_to_cityevents(xml_element), date, street)
        if len(lista) == 0:
            print(RED_COLOR_TAG + "Nothing found." + CLOSE_TAG)
            sys.exit()
        else:
            for i in lista:
                i.print_event()


if __name__ == "__main__":
    main()
