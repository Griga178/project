from .models import db, SubCategory, okpd_2, Ktru, Category, ProductPart, Characteristic, Value, SubCategoryCharacteristic

def load_sub_categories_v2(sub_categories: list) -> None:

    okpd2_set = set()
    ktru_set = set()
    productPart_set = set()
    category_set_of_tuples = set()
    for sub_category in sub_categories:
        okpd2_set.add(sub_category['okpd_2'])
        ktru_set.add(sub_category['ktru'])
        productPart_set.add(sub_category['product_part'])
        category_set.add(
        (sub_category['category_name'],
        sub_category['okpd_2'],
        sub_category['product_part'])
        )

    # for sub_category in sub_categories:
    #     okpd2_set.add(sub_category['okpd_2'])
    #     ktru_set.add(sub_category['ktru'])
    #     productPart_set.add(sub_category['product_part'])

    okpd2_dict = get_okpd2_by_list(okpd2_set)
    ktru_dict = get_ktru_by_list(ktru_set)
    productPart_dict = get_productPart_by_list(productPart_set)
    category_dict = get_category_by_list(category_set ,okpd2_dict, productPart_dict)
    # sub_category_dict = get_sub_category_by_list(category_set, category_dict)

def get_okpd2_by_list(okpd2_set):
    print('Сбор окпд2')
    l = len(okpd2_set)
    c = 1
    we_need_commit = False
    out_dict = {}
    for okpd2 in okpd2_set:
        c += 1
        okpd2_item = db.session.query(okpd_2).filter_by(number=okpd2).first()

        if not okpd2_item:
            we_need_commit = True
            okpd2_item = okpd_2(name=okpd2)
            db.session.add(okpd2_item)

        out_dict[okpd2] = okpd2_item
        print(f'{c}/{l} шт.', end='\r')

    if we_need_commit:
        db.session.commit()
    print('готово', c)
    for okpd2_key in out_dict:
        out_dict[okpd2_key] = out_dict[okpd2_key].id

    return out_dict

def get_ktru_by_list(income_set):
    print('Сбор КТРУ')
    l = len(income_set)
    c = 1
    out_dict = {}
    we_need_commit = False
    for item_key in income_set:
        c += 1
        db_item = db.session.query(Ktru).filter_by(number=item_key).first()

        if not db_item:
            we_need_commit = True
            db_item = Ktru(name=item_key)
            db.session.add(db_item)

        out_dict[item_key] = db_item
        print(f'{c}/{l} шт.', end='\r')
    if we_need_commit:
        db.session.commit()
    print('готово', c)
    for item_key in out_dict:
        out_dict[item_key] = out_dict[item_key].id

    return out_dict

def get_productPart_by_list(income_set):
    print('Сбор товарных частей')
    l = len(income_set)
    c = 1
    out_dict = {}
    we_need_commit = False
    for item_key in income_set:
        c += 1
        db_item = db.session.query(ProductPart).filter_by(number=item_key).first()

        if not db_item:
            we_need_commit = True
            db_item = ProductPart(name=item_key)
            db.session.add(db_item)

        out_dict[item_key] = db_item
        print(f'{c}/{l} шт.', end='\r')
    if we_need_commit:
        db.session.commit()
    print('готово', c)
    for item_key in out_dict:
        out_dict[item_key] = out_dict[item_key].id

    return out_dict

def get_category_by_list(category_set, okpd2_dict, productPart_dict):
    print('Сбор категорий')
    l = len(category_set)
    c = 1
    out_dict = {}
    we_need_commit = False
    for category in category_set:
        c += 1
        db_item = db.session.query(Category).filter_by(
        name=category[0], okpd_2_id=category[1]).first()
        if not db_item:
            we_need_commit = True
            db_item = Category(
                name=category[0],
                okpd_2_id=okpd2_dict[category[1],]
                product_part_id = productPart_dict[category[2]]
            )
            db.session.add(db_item)

        out_dict[(category[0], category[1])] = db_item
        print(f'{c}/{l} шт.', end='\r')

        for item_key in out_dict:
            out_dict[item_key] = out_dict[item_key].id
    if we_need_commit:
        db.session.commit()


        return out_dict
