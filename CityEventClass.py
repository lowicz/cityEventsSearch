#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

BLUE_COLOR_TAG = "\x1B[34;40m"
BOLD_TAG = "\x1B[1m"
CLOSE_TAG = "\x1B[0m"


class CityEvent(object):
    def __init__(self, event_date, event_description):
        prog = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        if prog.match(event_date):
            self.event_date = event_date
            self.event_description = event_description
        else:
            raise RuntimeError('Date must be in YYYY-MM-DD format')

    def description_search(self, pattern):
        return pattern.lower() in self.event_description.lower()

    def print_event(self):
        print BLUE_COLOR_TAG + BOLD_TAG + "Event Date: " \
            + CLOSE_TAG + str(self.event_date)
        print BLUE_COLOR_TAG + BOLD_TAG + "Event Description: " \
            + CLOSE_TAG + str(self.event_description)
