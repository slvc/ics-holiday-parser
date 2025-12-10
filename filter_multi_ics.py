import requests
from ics import Calendar, Event
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
    raw_cal = Calendar(resp.text)

    official_holidays = Calendar()
    memorial_days = Calendar()

    for e in raw_cal.events:
        desc = e.description or ''
        matched = any(k in desc for k in keywords)

        if matched:
            official_holidays.events.add(e)
        else:
            memorial_days.events.add(e)

    return official_holidays, memorial_days

def main():
    os.makedirs('public', exist_ok=True)

    for region_key, region_item in CONFIG_DICT.items():
        official_holidays, memorial_days = filter_calendar(
            region_item['source'],
            region_item['keywords'],
        )

        with open(f'public/{region_key}-official_holidays.ics', 'w', encoding='utf-8') as f:
            f.writelines(official_holidays.serialize_iter())

        with open(f'public/{region_key}-memorial_days.ics', 'w', encoding='utf-8') as f:
            f.writelines(memorial_days.serialize_iter())

if __name__ == '__main__':
    main()
