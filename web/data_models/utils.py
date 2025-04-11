from .models import db, SubCategory, okpd_2, Ktru, Category, ProductPart, Characteristic, Value, SubCategoryCharacteristic

import time

def load_sub_categories(sub_categories: list) -> dict:
    errors = []
    for sub_category in sub_categories:

        print(sub_category.get('name'))
        if sub_category['okpd_2']:
            okpd_item = get_or_create_okpd_2(sub_category['okpd_2'])
        else:
            errors.append({'error': "okpd_2", 'message': f'okpd_2 is none, ккн: {sub_category["name"]}'})
            continue

        if sub_category['ktru']:
            sub_category['ktru'] = get_or_create_ktru(sub_category['ktru'])

        if sub_category['product_part']:
            product_part_item = get_or_create_product_part(sub_category['product_part'])
        else:
            errors.append({'error': "product_part", 'message': f'product_part is none, ккн: {sub_category["name"]}'})
            continue

        if sub_category['category_name']:
            category_item = get_or_create_category(
            sub_category['category_name'],
            okpd_2_id = okpd_item.id,
            product_part_id = product_part_item.id)
        else:
            errors.append({'error': "category_name", 'message': f'category_name is none, ккн: {sub_category["name"]}'})
            continue

        # если ККН уже был создан, изменения не учитываются
        # 2 вар(to do): сравнить все, заменить, создать файл с изменениями
        sub_category_item = db.session.query(SubCategory).filter_by(name=sub_category.get('name')).first()
        if not sub_category_item:
            sub_category_item = SubCategory(
                number=sub_category.get('number'),
                name=sub_category.get('name'),
                code=sub_category.get('code'),
                measure=sub_category.get('measure'),
                actualization_date=sub_category.get('actualization_date'),  # Или другое значение
                russian=sub_category.get('russian'),
                kkn_code=sub_category.get('kkn_code'),

                category_id=category_item.id,  # Необходимо указать, как получить category_id
                ktru_id=sub_category.get('ktru_id')  # Необходимо указать, как получить ktru_id
            )
            if sub_category.get('ktru_id'):
                sub_category_item.ktru_id = sub_category['ktru'].id
            # Сохраняем объект в базе данных
            db.session.add(sub_category_item)
            db.session.commit()


        # Загрузка характеристик
        for char in sub_category['chars']:
            # print('Создание Наименования характеристик',char)
            # Создание Наименования
            char['category_id'] = category_item.id
            if char['value_1'] or char['value_2']:
                char['type'] = 'min_max'
            elif char['value_3']:
                char['type'] = 'list'
            elif char['value_4']:
                char['type'] = 'one'
            char_item = get_or_create_characteristic(**char)
            # Добавление возможных значений в Категорию
            # print(char_item.__dict__)
            value_items = []
            if char['type'] == 'min_max':
                value_item = get_or_create_value(name=None, char_id = char_item.id)
                value_item.temp_min = char['value_1']
                value_item.temp_max = char['value_2']
                value_items.append(value_item)
            elif char['type'] == 'one':
                v_name = char['value_4']
                value_item = get_or_create_value(name=v_name, char_id = char_item.id)
                value_items.append(value_item)
            elif char['type'] == 'list':
                for value in char['value_3']:
                    v_name = value
                    value_item = get_value(name=v_name, char_id = char_item.id)
                    if not value_item:
                        value_item = create_value(name=v_name, char_id = char_item.id)
                    value_items.append(value_item)
                else:
                    db.session.commit()

            # Связь ккн - имя_характ - значение_характ
            time.sleep(0.5)
            for val_list_item in value_items:
                # print(val_list_item.__dict__)
                sb_char_val = get_subCat_char_value(
                    value_id = val_list_item.id,
                    characteristic_id = char_item.id,
                    sub_category_id = sub_category_item.id,
                    min = val_list_item.temp_min if hasattr(val_list_item, 'temp_min') else None,
                    max = val_list_item.temp_max if hasattr(val_list_item, 'temp_max') else None
                    )
                if not sb_char_val:
                    create_subCat_char_value(
                        value_id = val_list_item.id,
                        characteristic_id = char_item.id,
                        sub_category_id = sub_category_item.id,
                        min = val_list_item.temp_min if hasattr(val_list_item, 'temp_min') else None,
                        max = val_list_item.temp_max if hasattr(val_list_item, 'temp_max') else None
                        )
            else:
                db.session.commit()

def get_or_create_okpd_2(number, name=None, is_final=False, comment=None, parent_okpd_id=None):
    # Поиск объекта по номеру
    okpd_item = db.session.query(okpd_2).filter_by(number=number).first()

    if okpd_item:
        # Если объект найден, возвращаем его
        return okpd_item
    else:
        # Если объект не найден, создаем новый
        new_okpd_item = okpd_2(
            number=number,
            name=name,
            is_final=is_final,
            comment=comment,
            parent_okpd_id=parent_okpd_id
        )

        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_okpd_item)
        db.session.commit()

        return new_okpd_item

def get_or_create_ktru(number, name=None):
    # Поиск объекта по номеру
    ktru_item = db.session.query(Ktru).filter_by(number=number).first()
    if ktru_item:
        # Если объект найден, возвращаем его
        return ktru_item
    else:
        # Если объект не найден, создаем новый
        new_ktru_item = Ktru(
            number=number,
            name=name,
        )

        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_ktru_item)
        db.session.commit()

        return new_ktru_item

def get_or_create_category(name, okpd_2_id, product_part_id, ktru_item = None):
    category_item = db.session.query(Category).filter_by(name=name, okpd_2_id=okpd_2_id).first()
    if category_item:
        # Если объект найден, возвращаем его
        return category_item
    else:
        # Если объект не найден, создаем новый
        new_category_item = Category(
            name=name,
            okpd_2_id=okpd_2_id,
            product_part_id = product_part_id
        )
        if ktru_item:
            new_category_item.ktru_id = ktru_item.id
        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_category_item)
        db.session.commit()

        return new_category_item

def get_or_create_product_part(name):
    product_part_item = db.session.query(ProductPart).filter_by(name=name).first()
    if product_part_item:
        # Если объект найден, возвращаем его
        return product_part_item
    else:
        # Если объект не найден, создаем новый
        new_product_part_item = ProductPart(
            name=name
        )
        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_product_part_item)
        db.session.commit()

        return new_product_part_item

def get_or_create_characteristic(**kw):

    char_item = db.session.query(Characteristic).filter_by(
        name=kw['name'],
        category_id=kw['category_id']).first()
    if char_item:
        return char_item
    else:
        new_char_item = Characteristic(
            name=kw['name'],
            category_id=kw['category_id'],
            measure=kw['measure'],
            type=kw['type'],
        )
        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_char_item)
        db.session.commit()

        return new_char_item

def get_or_create_value(**kw):
    value_item = db.session.query(Value).filter_by(
        name=kw['name'],
        characteristic_id=kw['char_id']).first()
    if value_item:
        return value_item
    else:
        new_value_item = Value(
            name=kw['name'],
            characteristic_id=kw['char_id']
        )
        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_value_item)
        db.session.commit()

        return new_value_item
def get_value(**kw):
    value_item = db.session.query(Value).filter_by(
        name=kw['name'],
        characteristic_id=kw['char_id']).first()
    if value_item:
        return value_item
    else:
        return None
def create_value(**kw):

    new_value_item = Value(
        name=kw['name'],
        characteristic_id=kw['char_id']
    )
    # Добавляем новый объект в сессию и сохраняем в БД
    db.session.add(new_value_item)
    return new_value_item

def get_or_create_subCat_char_value(
    sub_category_id, characteristic_id, value_id,
    min, max):
    sbCatChar_item = db.session.query(SubCategoryCharacteristic).filter_by(
        value_id=value_id,
        characteristic_id=characteristic_id,
        sub_category_id=sub_category_id,
        min=min, max=max).first()
    if sbCatChar_item:
        return sbCatChar_item
    else:
        new_sbCatChar_item = SubCategoryCharacteristic(
            value_id=value_id,
            characteristic_id=characteristic_id,
            sub_category_id=sub_category_id,
            min=min, max=max
        )
        # Добавляем новый объект в сессию и сохраняем в БД
        db.session.add(new_sbCatChar_item)
        db.session.commit()

        return new_sbCatChar_item

def get_subCat_char_value(
    sub_category_id, characteristic_id, value_id,
    min, max):
    sbCatChar_item = db.session.query(SubCategoryCharacteristic).filter_by(
        value_id=value_id,
        characteristic_id=characteristic_id,
        sub_category_id=sub_category_id,
        min=min, max=max).first()
    if sbCatChar_item:
        return sbCatChar_item
    else:
        return None
def create_subCat_char_value(
    sub_category_id, characteristic_id, value_id,
    min, max):

    new_sbCatChar_item = SubCategoryCharacteristic(
        value_id=value_id,
        characteristic_id=characteristic_id,
        sub_category_id=sub_category_id,
        min=min, max=max
    )
    # Добавляем новый объект в сессию и сохраняем в БД
    db.session.add(new_sbCatChar_item)
    # db.session.commit()

    return new_sbCatChar_item
