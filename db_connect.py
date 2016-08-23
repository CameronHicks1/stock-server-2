import sqlite3
import json

def add_symbol(values):
    """ Adds symbol to stocks table
        - values must be array consisting of:
        [symbol, ask, bid, daysRange, dividendShare, dividendYield, name
        previousClose, yearLow, yearHigh]
    """
    conn = sqlite3.connect('symbols.db')
    command = "INSERT INTO stocks VALUES "
    c = conn.cursor()

    values_list = "("

    for value in values:
        if value == values[-1]:
            values_list = values_list + '"' + str(value) + '")'
        else:
            values_list = values_list + '"' + str(value) + '", '

    command += values_list
    
    try:
        c.execute(command)
    except sqlite3.OperationalError:
        print('ERROR: Database does not exist')
    except sqlite3.IntegrityError:
        print('ERROR: Stock already exists in database')

    conn.commit()
    conn.close

def update_symbol(values):
    """Updates all stats except name & symbol"""
    conn = sqlite3.connect('symbols.db')
    command = "UPDATE stocks SET "
    c = conn.cursor()

    values_list = 'ask = "' + str(values[1]) + '", bid = "' + str(values[2]) + '", daysRange = "' + str(values[3]) + '", dividendShare = "' + str(values[4]) + '", dividendYield = "' + str(values[5]) + '", previousClose = "' + str(values[7]) + '", yearLow = "' + str(values[8]) + '", yearHigh = "' + str(values[9]) + '" WHERE symbol = "' + str(values[0]) + '";'

    command += values_list

    try:
        c.execute(command)
    except sqlite3.OperationalError:
        print('ERROR: Database does not exist')

    conn.commit()
    conn.close()

def delete_symbol(symbol):
    """Deletes symbol entry from stocks table"""
    conn = sqlite3.connect('symbols.db')
    command = 'DELETE FROM stocks WHERE symbol = "' + str(symbol) + '";'
    c = conn.cursor()
    
    try:
        c.execute(command)
    except sqlite3.OperationalError:
        print("Error: Table does not exist")
    
    conn.commit()
    conn.close()

def retrieve_symbol(symbol):
    """Retrieves data from stocks table"""
    conn = sqlite3.connect('symbols.db')
    command = 'SELECT * FROM stocks WHERE symbol = "' + str(symbol) + '";' 
    command2 = 'SELECT name FROM stocks WHERE symbol = "' + str(symbol) + '";'
    
    c = conn.cursor()
    c.execute(command)

    data = str(c.fetchone()).replace('(', '[').replace(')', ']')
    data = data.replace("'", "")
    data = data.split(',')
    
    j_dict = {str(symbol): {'symbol': str(symbol), 'ask': data[1], 'bid': data[2], 'range': data[3], 'dividend': data[4], 'yield': data[5], 'name': data[6], 'last_close': data[7], 'low': data[8], 'high': data[9].replace(']', '')}}

    data = json.dumps(j_dict)
        
    conn.close()

    return data

def select_all():
    """Selects all stocks from symbols.db for stock homepage"""
    conn = sqlite3.connect('symbols.db')
    command = 'SELECT * FROM stocks ORDER BY symbol;'

    c = conn.cursor()
    c.execute(command)
    
    data = str(c.fetchall()).replace('(', '[').replace(')', ']')
    
    conn.close()

    return data

def select_all_json():
    """Selects all stocks from symbols.db for stock homepage and returns json"""
    conn = sqlite3.connect('symbols.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    
    rows = db.execute('''
        SELECT * FROM stocks ORDER BY symbol;
        ''').fetchall()

    conn.commit()
    conn.close()

    return json.dumps([dict(ix) for ix in rows])

def retrieve_symbol_json(symbol):
    """Retrieves data from stocks table and returns json object
       *** Function does not currently work ***
    """
    conn = sqlite3.connect('symbols.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    command = ('SELECT * FROM stocks WHERE symbol = "' + str(symbol) + '";')

    rows = db.execute(command).fetchall()
    print(rows)

    conn.commit()
    conn.close()
    
    return json.dumps([dict(ix)] for ix in rows)

def return_all_symbols():
    """Retrieves all symbols from stocks table"""
    conn = sqlite3.connect('symbols.db')
    db = conn.cursor()

    command = 'SELECT symbol FROM stocks ORDER BY symbol;'

    data = db.execute(command).fetchall()
    return_data = []
    for symbol in data:
        return_data.append(symbol[0])
    
    conn.commit()
    conn.close()

    return return_data
