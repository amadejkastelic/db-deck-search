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
override_player_name = None
override_start_id = None
override_num_scanned = None
override_id_prefix = None
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

player_name = override_player_name or input('Enter player name: ')
print('Searching replays for: {}'.format(player_name))

def scrape(url, out_file):
    driver.get(url)
    time.sleep(0.5)
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

with open(out_file_name, "w") as out_file:
    for i in range(num):
        scrape(url.format(start_id_prefix, start_id-i), out_file)
