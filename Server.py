from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render
from db_connect import *
from Symbol_Module import Symbol


def stock_table(request):
    """Shows table of all stocks"""
    data = select_all_json()
    data = data.replace('&#44;', ',').replace('&#39;', "'")
    stocks = return_all_symbols()
    
    result = render('static/templates/stock_table.pt',
                    {'data': data},
                    request=request)
    response = Response(result)
    response.content_type = 'html'

    return response


def stock_home(request):
    """Returns all stocks from database to homepage"""
    data = return_all_symbols()

    result = render('static/templates/stock_home.pt',
                    {'data': data},
                    request=request)
    response = Response(result)
    response.content_type = 'html'

    return response


def stock_page(request):
    """Returns individual stats for stock matching URL"""
    symbol = '%(symbol)s' % request.matchdict
    
    data = retrieve_symbol(symbol)
    data = data.replace('&#44;', ',')

    result = render('static/templates/stock_page.pt',
                    {'data': data, 'symbol': symbol},
                    request=request)

    response = Response(result)
    response.content_type = 'html'

    return response


def post_handler(request):
    """Accepts JSON POST request and deals with data accordingly"""
    js = request.json_body

    if "update_site" in str(js):
        js_object = js_object = str(js).replace("{'update_site': '", "")
        symbol = str(js_object).replace("'}", "")
        symbol = symbol.upper()

        obj = Symbol(str(symbol), True)
        obj.update_db_entry()

    elif "create_site" in str(js):
        js_object = js_object = str(js).replace("{'create_site': '", "")
        symbol = str(js_object).replace("'}", "")
        symbol = symbol.upper()

        obj = Symbol(str(symbol))
        # obj.update_db_entry()

    elif "delete_site" in str(js):
        js_object = js_object = str(js).replace("{'delete_site': '", "")
        symbol = str(js_object).replace("'}", "")
        symbol = symbol.upper()

        obj = Symbol(str(symbol), True)
        obj.delete_db_entry()

    return Response("{response: 'OK'}")

if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_chameleon')
    config.include('pyramid_assetviews')
    
    config.add_route('stock_home', '/stocks/')
    config.add_view(stock_home, route_name='stock_home')

    config.add_route('stock_page', '/stocks/{symbol}')
    config.add_view(stock_page, route_name='stock_page')

    config.add_route('stock_table', '/table/')
    config.add_view(stock_table, route_name='stock_table')

    config.add_view(post_handler)
    
    app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
