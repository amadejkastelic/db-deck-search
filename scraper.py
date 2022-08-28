import datetime
import json
import time
import typing

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Overrides
override_card_names = None
override_start_id = None
override_num_scanned = None
override_file_name = None

options = Options()
options.add_argument('--headless')

capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    desired_capabilities=capabilities, 
    options=options,
)

card_names = override_card_names or input('Entered card name / deck name separated by ,: ').split(',')
print(card_names)

def scrape(url, out_file):
    driver.get(url)
    time.sleep(0.2)
    for entry in driver.get_log('browser'):
        deck_name = parse_deck_name(console_entry=entry) or 'No name'
        if all(card_name.lower() in entry.get('message', '').lower() for card_name in card_names):
            res = '{} - {} - {}\n'.format(datetime.datetime.now(), deck_name, url)
            out_file.write(res)
            print(res)

def parse_deck_name(console_entry: typing.Dict) -> str:
    message = console_entry.get('message', '')
    if not message or '\\\"action\\\":\\\"Success\\\"' not in message:
        return ''
    pattern = '\\\"name\\\":\\\"'
    start = message.find(pattern) + len(pattern)
    message = message[start:]
    pattern = '\\\",'
    end = message.find(pattern)
    message = message[:end]
    return message

url = 'https://www.duelingbook.com/deck?id={}'
start_id = override_start_id or int(input('Enter start id: '))
num = override_num_scanned or int(input('Enter number of scanned decks: '))
out_file_name = override_file_name or input('Set output file name: ')

with open(out_file_name, "w") as out_file:
    for i in range(num):
        scrape(url.format(start_id-i), out_file)
