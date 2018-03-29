from datetime import datetime
from workalendar.asia import Singapore
from functools import reduce
import csv
from dateutil.tz import tzoffset

def _holidays_for_year(year):
    cal = Singapore()
    return cal.holidays(year)

def _parse_holidays(holidays):
    cleaned_dates = list(map(lambda date: _clean_holiday_date(date), holidays))
    parsed_dates = []
    for cleaned_date in cleaned_dates:
        (date, name) = cleaned_date
        parsed_date = {}
        parsed_date['name'] = name
        parsed_date['date'] = date
        parsed_dates.append(parsed_date)
    return parsed_dates

def _clean_holiday_date(holiday_date):
    (date, name) = holiday_date
    timezone = tzoffset('UTC+8', 8*3600)
    date = datetime.combine(date, datetime.min.time()).isoformat()
    return (date, name)

def holidays_for_years(years):
    holidays_per_year = map(lambda year: _parse_holidays(_holidays_for_year(year)), years)
    all_holidays = reduce(lambda x, y: x + y, holidays_per_year)
    return all_holidays

def save_holidays(holidays, outfile='data/workalendar_sg.csv'):
    with open(outfile, 'w') as csv_file:
        field_names = holidays[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=field_names, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(holidays)

current_year = datetime.now().year
years = list(range(2000, current_year))
holidays = holidays_for_years(years)
save_holidays(holidays)
