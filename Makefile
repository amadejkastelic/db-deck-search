SHELL := /bin/bash

scrape:
	pipenv run python scraper.py

review:
	pipenv run python deck_parser.py

replay-finder:
	pipenv run python replay_finder.py
