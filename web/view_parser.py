from .view_main_page import *
from .parse_v2 import Parser_ver_2

parse_app = Parser_ver_2(
    app = app,
    db = db,
    Contrant_card = Contrant_card,
    Product = Product,
    Company = Company,
    )

@app.route('/parse_page')
def get_parse_page():
    return render_template('parser.html', **parse_app.get_info())

@app.route('/get_sum_info', methods = ['GET'])
def get_sum_info():
    return parse_app.get_sum_info()

@app.route('/check_info', methods = ['GET'])
def check_info():
    return parse_app.get_info()

@app.route('/start_parse_numbers', methods = ['GET', 'POST'])
def start_parse_numbers():
    message = parse_app.set_dates(**request.form)
    parse_app.parse_contract_numbers()
    return parse_app.get_sum_info()


@app.route('/stop_parse_numbers', methods = ['GET'])
def stop_parse_numbers():
    parse_app.app_status = 11
    return parse_app.get_info()

@app.route('/refresh_parse_numbers', methods = ['GET'])
def refresh_parse_numbers():
    parse_app.refresh_app()
    parse_app.app_status = 0
    return parse_app.get_info()

@app.route('/start_parse_products', methods = ['GET', 'POST'])
def start_parse_products():
    parse_app.parse_products()
    return parse_app.get_sum_info()
