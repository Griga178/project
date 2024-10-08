import re
# from convert import string_to_float, clean_string
from ..convert_data import *

def get_product_name_country(cell):
    # '3. Источник вторичного электропитания резервированный Smartec ST-PS103\nСтрана происхождения: КИТАЙ (156)'
    info = cell.split('\n')
    for el in info:
        split_el = re.findall(r'\w+|\.+|\,+|\-+', el)
        if not split_el:
            info.remove(el)
    # info = re.findall(r'\w+|\.+|\,+|\-+',cell)

    print(info)
    values = {}

    # ktru_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}-\d{8}', cell)
    # values['ktru'] = ktru_res[0] if ktru_res else None
    # okpd_2_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}', cell)
    # values['okpd_2'] = okpd_2_res[0] if okpd_2_res else None

    # reg_check = re.findall('^\d+. ', info[0])
    # if reg_check:
    #     values['name'] = info[0][len(reg_check[0]):]
    # else:
    #     values['name'] = info[0]


    # if len(info) > 1:
    #     values['country_producer'] = info[1].replace('Страна происхождения: ', '') if 'Страна' in info[1] else None
    # else:
    #     values['country_producer'] = None
    return values

def get_ktru_okpd_2(product_info, cell):
    info = {}

    ktru_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}-\d{8}', cell)
    if ktru_res:
        info['ktru'] = ktru_res[0]
    okpd_2_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}', cell)
    if okpd_2_res:
        info['okpd_2'] = okpd_2_res[0]

    return info

def get_product_type(cell):
    info = {}
    info['type'] = clean_string(cell)

    return info

def get_quantity_measure(cell):
    info = {}
    info['quantity'] = string_to_float(cell)
    cell_content = cell.split(' ')
    info['measure'] = cell_content[-1]

    return info

def get_price(cell):
    info = {}
    info['price'] = string_to_float(cell)

    return info

def get_cost_tax(cell):
    info = cell.split('\n')
    values = {}
    values['cost'] = string_to_float(info[0])

    if len(info) > 1:
        values['tax'] = info[1].replace('Ставка НДС: ', '') if 'Ставка' in info[1] else None
    else:
        values['tax'] = None

    return values
