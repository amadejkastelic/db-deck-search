SHELL := /bin/zsh

virtualenv:
	virtualenv -p python3 dbscraper

deps:
	pip install selenium webdriver-manager

scrape:
	python3 scraper.py

review:
	python3 parser.py
