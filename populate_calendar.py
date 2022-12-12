import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduling.settings')

import django 
django.setup()

from calendar_app import models
from datetime import datetime
import calendar 

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# this function takes year and calendar_values db with all the days and slug values
def populate(year):
# loop through each month of the calendar year
       for a_month in months:
# create a calendar object
              cal_obj = calendar.Calendar()
# fetch one month of dates from its year and month
              for week in cal_obj.monthdays2calendar(year, a_month):
# week is a tuple of two values. 1. day and 2 is day in the week.
# we create a loop to access both values of the tuple week 
                     for d, w in week:
# when month begins other than monday, w will be 0 
                            if d != 0:
                                   calendar_values = models.Calendar() # create a database Calendar object
                                   calendar_values.day = d # vaue of day
                                   calendar_values.month = a_month # value of month 
                                   calendar_values.year = year # value of year
                                   if d < 10:
                                          calendar_values.slug = f"{year}-{a_month}-0{d}" # slug value
                                   else:
                                          calendar_values.slug = f"{year}-{a_month}-{d}" 
                                   calendar_values.week_day = w # day in the week 
                                   calendar_values.save() # save the day in the Calendar table
# we calendar_values the db by the following years
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
# loop through each year and call calendar_values function to write and commit data on db
for year in years:
       populate(year)