import datetime
import random
import time
import typing

import fake_useragent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Overrides
override_player_name = None
override_start_id = None
override_num_scanned = None
override_id_prefix = None
override_file_name = None
try:
    import overrides

    override_player_name = overrides.player_name
    override_start_id = overrides.start_id
    override_num_scanned = overrides.num_scanned
    override_id_prefix = overrides.id_prefix
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
driver.set_page_load_timeout(10)

player_name = override_player_name or input('Enter player name: ')
print('Searching replays for: {}'.format(player_name))


def scrape(url: str, out_file: typing.IO) -> None:
    driver.get(url)
    time.sleep(1)
    for entry in driver.get_log('browser'):
        if player_name.lower() in entry.get('message', '').lower():
            res = '{} - {}\n'.format(datetime.datetime.now(), url)
            out_file.write(res)
            print(res)
            break


url = 'https://www.duelingbook.com/replay?id={}{}'
start_id = override_start_id or int(input('Enter start id: '))
num = override_num_scanned or int(input('Enter number of scanned decks: '))
start_id_prefix = override_id_prefix or input('Enter start id prefix: ')
out_file_name = override_file_name or input('Set output file name: ')

with open(out_file_name, 'w') as out_file:
    for i in range(num):
        scrape(url.format(start_id_prefix, start_id - i), out_file)
