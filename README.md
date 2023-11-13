# DB-Deck-Search

## Prerequisites
- Python3.11
- Pipenv
- Google Chrome / Chromium

## How to use
- Clone the repository
- Create the virtual environment and install dependencies
```bash
pipenv install
```
- Use virtual environment
```bash
pipenv shell
```
- Run scraper
```bash
make scrape
```
- Review the output after scraping is done:
```bash
make review
```

# Obtaining the last deck id
- Navigate to https://duelingbook.com/
- Navigate to `Deck Constructor` and create a new empty deck
- Click the `Export Deck` button and select `Download Link`
- Copy the id query param from url
