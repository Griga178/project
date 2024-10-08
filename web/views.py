from .view_table import *

'''
    app -->
    models -->
    view_main_page -->
    view_parser -->
    view_table -->

    views --> __init__ --> app3.py
'''

# Стандартная таблица DataTable from JS - тяжелая, долго загружается
@app.route('/api/products')
def api_products():
    return {'data': [product.to_dict() for product in Product.query]}


@app.route('/products', methods = ('GET', 'POST'))
def products():

    return render_template('products.html', title = 'Товары')
