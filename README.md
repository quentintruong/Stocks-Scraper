## Solution to The Phantom Intern Challenge: #1: Stocks-Scraper

## Challenge Statement:
1. List top 10 stocks, priced between $100 and $200 and with the highest value variation in the last 30 days. Additional bonus points for predicting which stock is likely to vary the most during the next trading day.

## Program Clarifications
I chose the DOW as my set of stocks. 

I assumed 30 days to be 23 trading days. 

Program works as of 9 June 2017, xpaths and links of my chosen websites may change, so check that before use.

# Approach
Scrape the 30 stocks of the DOW using a webspider.

Use the scrapy item pipeline to hold items until all websites have been scraped. 

Sort all items according to highest average price variation and return the top as likely to vary the most during the next trading day.

Sort a ranged subset of the items according to highest average price variation and return the top 10.

Add request delay to prevent target website from banning spider and/or not fulfilling request.

## Requires: 

python3.5

scrapy

## To Run:
1. Clone directory
2. Run the following command in directory
```$ scrapy crawl stocks```
