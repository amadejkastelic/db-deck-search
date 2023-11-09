import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})


def review(driver, url):
    driver.get(url)
    open = True
    while open:
        try:
            driver.title
            time.sleep(0.1)
        except Exception:
            open = False


with open(input('Enter output file path of scraper.py: ')) as in_file:
    for url in in_file:
        if not url:
            continue
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        if '-' in url:
            print('Deck name: {}'.format(url.split(' - ')[1]))
            review(driver, url.split(' - ')[-1])
        else:
            review(driver, url)
