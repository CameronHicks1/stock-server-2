import urllib.request
import re
import json
from db_connect import add_symbol, update_symbol, delete_symbol, retrieve_symbol

class Symbol:
    """Stock with methods to call Yahoo!Finance API"""
    def __init__(self, symbol, exists=False):

        self.symbol = symbol.replace(".", '-').upper()
        # URL >> Yahoo query language.
        # SELECT * FROM yahoo.finance.quotes
        # WHERE symbol IN ("self.symbol");
        self.url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22' + self.symbol + '%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json'
        self.initialized = exists

        # Check if stock has been initialized
        if self.initialized:
            return
        else:
            # Create database entry if stock does not exist
            self.create_db_entry()
        
    def get_raw_data(self):
        """Queries Yahoo!Finance API for Symbol, returns as JSON"""
        data = urllib.request.urlopen(self.url).read().decode('utf-8')
        data = json.loads(data)

        return data

    def get_data(self):
        """Transforms raw data into array for create_db_entry"""
        data = self.get_raw_data()

        name = data['query']['results']['quote']['Name']
        ask = data['query']['results']['quote']['Ask']
        bid = data['query']['results']['quote']['Bid']
        days_range = data['query']['results']['quote']['DaysRange']
        dividend_share = data['query']['results']['quote']['DividendShare']
        dividend_yield = data['query']['results']['quote']['DividendYield']
        previous_close = data['query']['results']['quote']['PreviousClose']
        year_low = data['query']['results']['quote']['YearLow']
        year_high = data['query']['results']['quote']['YearHigh']

        modified_data = [self.symbol, ask, bid, days_range, dividend_share,
                         dividend_yield, name.replace(',', '&#44;').replace("'", "&#39;"), previous_close, year_low,
                         year_high.replace(']', '')]

        return modified_data

    def create_db_entry(self):
        """Adds symbol to stocks table in database"""
        data = self.get_data()
        add_symbol(data)
        self.initialized = True

    def update_db_entry(self):
        """Updates symbol in stocks database"""
        data = self.get_data()
        update_symbol(data)

    def delete_db_entry(self):
        """Removes symbol from stocks table in database"""
        delete_symbol(self.symbol)

    def retrieve_data(self):
        """Retrieves the data values from stocks table"""
        return retrieve_symbol(self.symbol)
