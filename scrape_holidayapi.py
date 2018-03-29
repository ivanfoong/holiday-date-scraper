import holidayapi
import os
from functools import reduce
import datetime
import time
import csv
from datetime import datetime
from dateutil.tz import tzoffset

def _holidays_for_year(year, country='SG', api_key=os.environ['HOLIDAY_API_KEY']):
    hapi = holidayapi.v1(api_key)
    parameters = {
        'country': country,
        'year':    year,
    }
    time.sleep(5)
    return hapi.holidays(parameters)

def _parse_holidays(holidays):
    parsed_holidays = []
    if 'holidays' not in holidays:
        return parsed_holidays
    for _, dates in holidays['holidays'].items():
        cleaned_dates = list(map(lambda date: _clean_holiday_date(date), dates))
        parsed_holidays = parsed_holidays + cleaned_dates
    return parsed_holidays

def _clean_holiday_date(holiday_date):
    timezone = tzoffset('UTC+8', 8*3600)
    holiday_date['date'] = datetime.strptime(holiday_date['date'], '%Y-%m-%d').replace(tzinfo=timezone).isoformat()
    holiday_date['observed'] = datetime.strptime(holiday_date['observed'], '%Y-%m-%d').replace(tzinfo=timezone).isoformat()
    return holiday_date

def holidays_for_years(years, country='SG', api_key=os.environ['HOLIDAY_API_KEY']):
    holidays_per_year = map(lambda year: _parse_holidays(_holidays_for_year(year, country, api_key)), years)
    all_holidays = reduce(lambda x, y: x + y, holidays_per_year)
    return all_holidays

def save_holidays(holidays, outfile='data/holidayapi_sg.csv'):
    with open(outfile, 'w') as csv_file:
        field_names = holidays[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=field_names, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(holidays)

current_year = datetime.now().year
years = list(range(2000, current_year))
holidays = holidays_for_years(years)
save_holidays(holidays)
