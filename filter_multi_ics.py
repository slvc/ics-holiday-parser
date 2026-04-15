import requests
from icalendar import Calendar, Event
import os

CONFIG_DICT = {
    'zh-tw.taiwan': {
        'source': 'https://calendar.google.com/calendar/ical/zh-tw.taiwan%23holiday@group.v.calendar.google.com/public/basic.ics',
        'keywords': ['\u570b\u5b9a\u5047\u65e5'],
    },
}

def filter_calendar(source_url, keywords):
    resp = requests.get(source_url)
    resp.raise_for_status()
    raw_cal = Calendar.from_ical(resp.content)

    official_holidays = Calendar()
    memorial_days = Calendar()

    for component in raw_cal.walk():
        if component.name != 'VEVENT':
            continue

        desc = str(component.get('DESCRIPTION', ''))
        matched = any(k in desc for k in keywords)

        if matched:
            official_holidays.add_component(component)
        else:
            memorial_days.add_component(component)

    return official_holidays, memorial_days

def main():
    os.makedirs('public', exist_ok=True)

    for region_key, region_item in CONFIG_DICT.items():
        official_holidays, memorial_days = filter_calendar(
            region_item['source'],
            region_item['keywords'],
        )

        with open(f'public/{region_key}-official_holidays.ics', 'wb') as f:
            f.write(official_holidays.to_ical())

        with open(f'public/{region_key}-memorial_days.ics', 'wb') as f:
            f.write(memorial_days.to_ical())

if __name__ == '__main__':
    main()