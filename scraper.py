import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')

capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    desired_capabilities=capabilities, 
    options=options,
)

card_name = input('Entered card name / deck name: ')

def scrape(url, out_file):
    driver.get(url)
    time.sleep(0.2)
    for entry in driver.get_log('browser'):
        if card_name in entry['message']:
            out_file.write('{} - {}\n'.format(datetime.datetime.now(), url))

url = 'https://www.duelingbook.com/deck?id={}'
start_id = int(input('Enter start id: '))
num = int(input('Enter number of scanned decks: '))

with open(input('Set output file name: '), "w") as out_file:
    for i in range(num):
        scrape(url.format(start_id-i), out_file)
