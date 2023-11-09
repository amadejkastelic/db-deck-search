import datetime
import logging
import random
import sys
import time
import typing

import fake_useragent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.Logger(__name__)

# Overrides
override_card_names = None
override_start_id = None
override_num_scanned = None
override_file_name = None
try:
    import overrides

    override_card_names = overrides.card_names
    override_start_id = overrides.start_id
    override_num_scanned = overrides.num_scanned
    override_file_name = overrides.file_name
except ImportError:
    pass

resolutions = [
    (1920, 1080),
    (1280, 720),
    (2560, 1440),
    (2560, 1080),
    (1920, 1200),
    (5120, 1440),
    (1366, 768),
    (1280, 800),
    (1600, 1200),
    (2048, 1152),
    (2560, 1600),
    (5120, 2160),
    (3840, 2400),
]

options = Options()
options.add_argument('--headless')
options.add_argument(f'user-agent={fake_useragent.UserAgent().random}')
options.add_argument('window-size={}'.format(','.join(map(str, random.choice(resolutions)))))
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options,
)
driver.set_page_load_timeout(3)

card_names = override_card_names or input('Enter card name / deck name separated by ,: ').split(',')
logger.info(card_names)


def scrape(url: str, out_file: typing.IO) -> None:
    driver.get(url)
    time.sleep(1)
    for entry in driver.get_log('browser'):
        deck_name = parse_deck_name(console_entry=entry) or 'No name'
        if all(card_name.lower() in entry.get('message', '').lower() for card_name in card_names):
            res = '{} - {} - {}\n'.format(datetime.datetime.now(), deck_name, url)
            out_file.write(res)
            logging.info(res)


def parse_deck_name(console_entry: typing.Dict) -> str:
    message = console_entry.get('message', '')
    if not message or '\\"action\\":\\"Success\\"' not in message:
        return ''
    pattern = '\\"name\\":\\"'
    start = message.find(pattern) + len(pattern)
    message = message[start:]
    pattern = '\\",'
    end = message.find(pattern)
    message = message[:end]
    return message


url = 'https://www.duelingbook.com/deck?id={}'
start_id = override_start_id or int(input('Enter start id: '))
num = override_num_scanned or int(input('Enter number of scanned decks: '))
out_file_name = override_file_name or input('Set output file name: ')

with open(out_file_name, 'w') as out_file:
    for i in range(num):
        scrape(url.format(start_id - i), out_file)
        if i % 1000 == 0:
            logging.debug(f'Current index: {i}')
