# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import operator # allows for fast sorting of tuples

class StocksPipeline(object):
    def __init__(self):
        self.itemContainer = {}
        self.CONST_MIN_PRICE = 100
        self.CONST_MAX_PRICE = 200
        self.CONST_NUM_STOCKS = 10

    def process_item(self, item, spider):
        # Get stocks symbol and store stock's data in a dict according to stock's symbol
        sym = item['sym'][0]
        self.itemContainer[sym] = item

        return item

    def close_spider(self, spider):
        # avgDiffPrices holds all price differences so we can determine which stock is most likely to vary during the next trading day
        # avgDiffPricesInRange holds price differences that are within range, so we can output them
        avgDiffPrices = []
        avgDiffPricesInRange = []

        # Iterate through all stocks
        for itemName in self.itemContainer:
            # accumDiffPrice is an accumulator for each stock
            # numDays is the number of trading days
            # sym is the stock's symbol
            # isOutOfRange determines whether or not to add the data to avgDiffPricesInRange
            accumDiffPrice = 0 
            numDays = len(self.itemContainer[itemName]['highPrice'])
            sym = self.itemContainer[itemName]['sym'][0]
            isOutOfRange = False

            # Iterate through data from each trading day
            for day in range(0, numDays):
                tempHighPrice = self.itemContainer[itemName]['highPrice'][day]
                tempLowPrice = self.itemContainer[itemName]['lowPrice'][day]

                # If the price does not fall within the accepted range, omit it from the ranged set
                if (tempLowPrice <= self.CONST_MIN_PRICE or tempHighPrice >= self.CONST_MAX_PRICE):
                    isOutOfRange = True

                accumDiffPrice += abs(tempHighPrice - tempLowPrice)

            # Omit out of range stocks from ranged subset
            if (isOutOfRange == False):
                avgDiffPricesInRange.append((sym, accumDiffPrice / numDays))

            avgDiffPrices.append((sym, accumDiffPrice / numDays))

        # Sort each list in decreasing order according to average variation
        avgDiffPrices.sort(key=operator.itemgetter(1), reverse=True)
        avgDiffPricesInRange.sort(key=operator.itemgetter(1), reverse=True)

        print("======START OF RESULTS OUTPUT======")

        if (len(avgDiffPrices) < 30):
            print("\nWARNING: Output may be incorrect due to target website not allowing our requests")
            print("Increasing 'DOWNLOAD_DELAY' in settings.py may help")

        # In case there are not 10 stocks that fall within the range, pick as many as you can
        minNumStocks = min(self.CONST_NUM_STOCKS, len(avgDiffPricesInRange))
        print("\nThe top " + str(self.CONST_NUM_STOCKS) + " stocks valued between " + str(self.CONST_MIN_PRICE) + " and " + str(self.CONST_MAX_PRICE) + " with the highest average price variation in the last 30 days are as follows:")
        for numStock in range(0, minNumStocks):
            print(str(numStock + 1) + ": '" + avgDiffPricesInRange[numStock][0] + "' varies " + str(avgDiffPricesInRange[numStock][1]))
        
        # Verify that there exists a stock to pick
        if (len(avgDiffPrices) > 0):
            # Pick the stock with the greatest average variation as the stock that is likely to vary the most during the next trading day
            print("\n'" + avgDiffPrices[0][0] + "' is likely to vary the most during the next trading day.\n")

        print("======END OF RESULTS OUTPUT======")

