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

'''
    Временны раздел
    Добавление auto-db-model-view
'''
from sqlalchemy.inspection import inspect

# from flask_admin import Admin
from flask_table import Table, Col
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
class FilterForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Filter')

@app.route('/gisp_proto', methods = ['GET', 'POST'])
def get_gisp_proto():

    # a = inspect(Product).c.keys()
    # a = inspect(Product).c.items()
    # print(a)
    # for column in inspect(Product).c:
    #     print(column.name, column.type)

    form = FilterForm()
    form = form
    if form.validate_on_submit():
        search_query = form.search.data
        # Здесь можно добавить логику для фильтрации данных на основе search_query
        print(search_query)
    filters = {}
    if request.method == 'POST':
        # Получение значений из формы
        characteristic = request.form.get('characteristic_1')
        if characteristic:
            filters['characteristic_1'] = characteristic
            print(request.form.to_dict())

    # products_query = Product.query
    if filters and False:
        products_query = products_query.filter_by(**filters)

    # products = products_query.all()
    products = {
        'id': 1,
        'name': "Комп",
    }

    return render_template('gisp_proto.html',
        title = 'Каталог продукции',
        products = products,
        form = form)


@app.route('/categories')
def show_categories():

    return render_template('categories.html', categories=SubCategory.query)
