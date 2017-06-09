import logging
import re # regex allows for data extraction

import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from stocks.items import StocksItem

class StocksSpider(scrapy.Spider):
    name = "stocks"
    dowSymbols = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DIS', 'DD', 'XOM', 'GE', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UTX', 'UNH', 'VZ', 'V', 'WMT']

    def start_requests(self):
        for sym in self.dowSymbols:
            url = 'http://www.nasdaq.com/symbol/' + sym + '/historical'
            yield scrapy.Request(url=url, callback=self.parse, meta={'sym': sym})

    def parse(self, response):
        # Set up ItemLoader and accumulators
        l = ItemLoader(item=StocksItem(), response=response)
        highPriceList = []
        lowPriceList = []

        for inc in range(1, 24): # (24-1) trading days => 30 days
            row = 1 + inc

            # Create xpaths
            highPath = '//div/div/table/tbody/tr[' + str(row) + ']//td[3]'
            lowPath = '//div/div/table/tbody/tr[' + str(row) + ']//td[4]'
            
            # Extract strings prices from html body
            highPrice = Selector(text=response.body).xpath(highPath).extract()
            lowPrice = Selector(text=response.body).xpath(lowPath).extract()

            # Regex select one or more digits, possibly a decimal, and zero or more digits
            highPrice = re.search('\d+\.?\d*', highPrice[0])
            lowPrice = re.search('\d+\.?\d*', lowPrice[0])

            # Convert regex return value to a float
            highPrice = float(highPrice.group(0))
            lowPrice = float(lowPrice.group(0))

            # Append values
            highPriceList.append(highPrice)
            lowPriceList.append(lowPrice)

        # Put values into ItemLoader
        l.add_value('sym', response.meta['sym'])
        l.add_value('highPrice', highPriceList)
        l.add_value('lowPrice', lowPriceList)
        return l.load_item()
