from datetime import timedelta, datetime
from dateutil import parser
from pprint import pprint
from time import sleep
import requests
import feedparser

BOT_TOKEN = 'XXXXXX:XXXXX' # Telegram Bot Token
CHANNEL_ID = '-XXXXXX:XXXXX' # Telegram Channel ID

FEED_URL_1="https://www.feedforall.com/sample.xml"

def send_message(message):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}')

def get_last_checkin(FEED):
    file = open('lastcheckin.txt', 'r') #Example: 2021-02-29 15:15:15+00:00
    last_checkin = file.read().strip()
    last_checkin = parser.parse(last_checkin)
    new_checkin  = last_checkin

    rss_feed = feedparser.parse(FEED)
    for entry in rss_feed.entries:
        entry_update = parser.parse(entry.updated)
        if entry_update > last_checkin:
            msg = f"Vul ID: {entry.get('title')}\n\nDescription: {entry.get('summary')}\n\nLink: {entry.get('link')}"
            send_message(msg)
            if entry_update > new_checkin:
                new_checkin = entry_update
    new_checkin = str(new_checkin)
    file = open('lastcheckin.txt', 'w')
    file.write(new_checkin)
    file.close()

#### MAIN ####
get_last_checkin(FEED_URL_1)
