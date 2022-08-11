#Ref: https://ljmocic.medium.com/make-telegram-bot-for-notifying-about-new-rss-feed-items-4cfbcc37f4fd

from datetime import timedelta, datetime
from dateutil import parser
from pprint import pprint
from time import sleep
import requests
import feedparser

BOT_TOKEN = 'XXXXXXXXXXXX' # the one you saved in previous step
CHANNEL_ID = '-XXXXXXXXXX' # don't forget to add this

FEED_URL_1="https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml"

def send_message(message):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}')

def news_update(FEED):
   rss_feed = feedparser.parse(FEED)
   for entry in rss_feed.entries:
      parsed_date = parser.parse(entry.updated)
      parsed_date = (parsed_date - timedelta(hours=8)).replace(tzinfo=None) # remove timezone offset
      now_date = datetime.utcnow()
      published_10_minutes_ago = now_date - parsed_date < timedelta(minutes=10)
      msg = f"Vul ID: {entry.get('title')}\n\nDescription: {entry.get('summary')}\n\nLink: {entry.get('link')}"
      if published_10_minutes_ago == True:
         send_message(msg)

news_update(FEED_URL_1)
