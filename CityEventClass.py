#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class CityEvent(object):
    def __init__(self, event_start_date, event_end_date, event_description):
            self.event_start_date = datetime.strptime(event_start_date,
                                                      '%Y-%m-%d')
            self.event_end_date = datetime.strptime(event_end_date, '%Y-%m-%d')
            self.event_description = event_description

    def description_search(self, pattern):
        return pattern.lower() in self.event_description.lower()

    def date_search(self, event_date):
        if self.event_start_date <= event_date <= self.event_end_date:
            return True
        else:
            return False

    def print_event(self):
        print("Event Start Date: " + self.event_start_date.strftime('%Y-%m-%d')
              + " Event End Date: " + self.event_end_date.strftime('%Y-%m-%d'))
        print("Event Description: " + str(self.event_description))
