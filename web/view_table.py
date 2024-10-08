from .view_parser import *
from sqlalchemy import desc

def reform_im_dict(imm_dict):
    '''
        переделка immutable-dict из форм DataTable
    '''
    filter_data = {'columns': {}, 'order': {}}
    # print(imm_dict.getlist('draw'))
    filter_dict = imm_dict.to_dict()
    # print(filter_dict.keys())
    for key, val in filter_dict.items():
        # print([key], val)
        if 'columns' in key:
            '''columns[0][data] -->
            'columns': {0:{'data': 'data'}}'''
            keys = key.split('[')
            keys = [i.replace(']','') for i in keys]
            clmn_id = keys[1]
            clmn_char = keys[2]
            if clmn_id not in filter_data['columns'].keys():
                filter_data['columns'][clmn_id] = {}
            if clmn_char == 'search':
                if 'search' not in filter_data['columns'][clmn_id]:
                    filter_data['columns'][clmn_id]['search'] = {}
                filter_data['columns'][clmn_id]['search'][keys[3]] = val
            else:
                filter_data['columns'][clmn_id][clmn_char] = val

        elif 'order' in key:
            '''Сортировка по столбцу
            'order': {'column': '0', 'dir': 'desc'}
            '''
            keys = key.split('[')
            keys = [i.replace(']','') for i in keys]
            clmn_id = keys[1]
            clmn_char = keys[2]
            filter_data['order'][clmn_char] = val
        elif key == 'search[value]':
            filter_data['search_value'] = val
        elif key == 'search[regex]':
            filter_data['search_regex'] = val

        else:
            filter_data[key] = val

    # print(filter_data)
    return filter_data

@app.route('/products_v2')
def products_v2():

    return render_template('products_v2.html', title = 'Товары 2.0')

@app.route('/api/products_v2', methods = ('GET', 'POST'))
def api_products_v2():


    searchValue = request.form["search[value]"] # строка для поиска

    # Переделанный словарь фильтрации
    filter_data = reform_im_dict(request.form)
    '''Применение фильтров к запросу SQL'''
    pq = Product.query.join(Contrant_card.products)
    # поиск по всем совпадениям
    if filter_data['search_value']:
        srch_val = filter_data['search_value'].upper().strip()
        from sqlalchemy import func
        pq = pq.filter(db.or_(
            Product.search_name.ilike(f'%{srch_val}%'),
            Product.okpd_2.like(f'%{srch_val}%'),
            Product.ktru.like(f'%{srch_val}%'),
            Product.country_producer.like(f'%{srch_val}%'),
            Product.contrant_card_id.like(f'%{srch_val}%'),
        ))
    # Фильтр по цене
    if filter_data['max_price'] != 'NaN':
        pq = pq.filter(Product.price <= filter_data['max_price'])
    if filter_data['min_price'] != 'NaN':
        pq = pq.filter(Product.price >= filter_data['min_price'])

    # Количество Найденных значений
    total_filtered = pq.count()
    # Сортировка по столбцу
    clmn_id = filter_data['order']['column']
    str_order_by = filter_data['columns'][clmn_id]['data']
    if str_order_by == 'contrant_card_date':
        obj_order_by = Contrant_card.date
    else:
        obj_order_by = getattr(Product, str_order_by)

    if filter_data['order']['dir'] == 'asc':
        pq = pq.order_by(obj_order_by)
    else:
        pq = pq.order_by(desc(obj_order_by))

    # Количество строк и номер страницы
    pq = pq.offset(filter_data['start']).limit(filter_data['length'])

    return {
    'draw': filter_data['draw'],
    'recordsTotal': Product.query.count(),
    'recordsFiltered': total_filtered,
    'data': [product.to_dict() for product in pq],
    }

@app.route('/api/products_edit_comment', methods = ('GET', 'POST'))
def edit_comment():
    id = request.form['id']
    comment = request.form['comment']
    prod_obj = Product.query.filter(Product.id == id).one()
    prod_obj.comment = comment
    db.session.add(prod_obj)
    db.session.commit()
    return {"added_comment": prod_obj.comment}
