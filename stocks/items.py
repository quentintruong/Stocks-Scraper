# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StocksItem(scrapy.Item):
 	# sym is the stock's symbol
 	# highPrice is the stock's high value
 	# lowPrice is the stock's low value
    sym = scrapy.Field()
    highPrice = scrapy.Field()
    lowPrice = scrapy.Field()
    pass
