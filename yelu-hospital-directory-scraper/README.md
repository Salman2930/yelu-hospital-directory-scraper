# Yelu Hospital Directory Scraper

## Overview

A Python-based web scraping project that extracts hospital information from Yelu India using Selenium, BeautifulSoup, and Pandas.

The scraper automates hospital search, handles pagination, visits individual profile pages, extracts business details, and exports the results to CSV format.

## Features

* Selenium browser automation
* Pagination handling
* Profile page navigation
* Hospital information extraction
* CSV export using Pandas
* Generic label-value extraction approach
* Missing field handling with fallback logic

## Technologies Used

* Python
* Selenium
* BeautifulSoup (BS4)
* Pandas

## Data Extracted

* Hospital Name
* Address
* Contact Number
* Website Address
* Email Status
* Profile URL

## Output

The scraper exports structured hospital data into a CSV file.

Sample dataset included:

* First 2737 hospital records
* Extracted from first 150 pages

## Project Workflow

1. Open Yelu India
2. Search for Hospitals
3. Collect hospital profile URLs
4. Handle pagination
5. Visit each hospital profile
6. Extract hospital details
7. Save data into CSV

## Learning Outcomes

* Selenium automation
* Pagination scraping
* Dynamic navigation
* Data cleaning
* CSV generation
* Real-world directory scraping
