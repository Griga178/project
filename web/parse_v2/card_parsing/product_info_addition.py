import re
from typing import Dict
import bs4

def get_product_name_country(td_tag: bs4.element.Tag) -> Dict:
    '''
        Ищем:
        ктру, окпд2, страну происхождения в ячейке с именем.
        Если находим, "вырезаем" в отдельную "переменную"

    '''
    split_cell = ' '.join(td_tag.text.split())

    info = td_tag.text.split('\n')
    values = {
        'country_producer': None,
        'ktru': None,
        'okpd_2': None,
    }

    # Поиск КТРУ
    ktru_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}-\d{8}', split_cell)
    values['ktru'] = ktru_res[0] if ktru_res else None
    # Поиск ОКПД 2
    okpd_2_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}', split_cell)
    values['okpd_2'] = okpd_2_res[0] if okpd_2_res else None

    # Поиск Страны происхождения
    rule = r'Страна происхождения: [А-Я ]+ \(\d+\)'
    country_producer_text = re.findall(rule, split_cell)
    if country_producer_text:
        values['country_producer'] = country_producer_text[0].replace('Страна происхождения: ','')

    # Поиск Имени
    name_tag = td_tag.div.find_all('div', recursive = False)
    if len(name_tag) == 1:
        values['name'] = ' '.join(name_tag[0].text.split())
    elif len(name_tag) == 2:
        values['name'] = ' '.join(name_tag[1].text.split())
    else:
        values['name'] = ' '.join(td_tag.div.text.split())

    values['search_name'] = values['name'].upper()
    return values

def get_ktru_okpd_2(td_tag: bs4.element.Tag) -> Dict:
    split_cell = ' '.join(td_tag.text.split())
    info = {}

    ktru_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}-\d{8}', split_cell)
    if ktru_res:
        info['ktru'] = ktru_res[0]
    okpd_2_res = re.findall(r'\d{2}.\d{2}.\d{2}.\d{3}', split_cell)
    if okpd_2_res:
        info['okpd_2'] = okpd_2_res[0]

    return info

def get_product_type(td_tag: bs4.element.Tag) -> Dict:
    split_cell = ' '.join(td_tag.text.split())
    info = {}
    info['type'] = split_cell

    return info

def get_quantity_measure(td_tag: bs4.element.Tag) -> Dict:
    split_cell = ' '.join(td_tag.text.split())
    info = {}
    quantity = re.findall(r'\d+,\d+|\d+\.\d+|\d+', split_cell)

    if quantity:
        quantity = ''.join(quantity).replace(',', '.')

        info['quantity'] = float(quantity)
    else:
        quantity = ''
        info['quantity'] = None

    measure = split_cell.replace(quantity, '')
    info['measure'] = measure.strip()

    return info

def get_price(td_tag: bs4.element.Tag) -> Dict:
    info = {}
    split_cell = ''.join(td_tag.text.split())
    price = re.findall(r'\d+,\d+|\d+\.\d+|\d+', split_cell)
    if price:
        info['price'] = float(price[0].replace(',', '.'))
    else:
        info['price'] = None

    return info

def get_country_producer(td_tag: bs4.element.Tag) -> Dict:
    info = {}
    split_cell = ' '.join(td_tag.text.split())
    rule = r'[а-яА-Я ]+, \(\d+,\)'
    country_producer_text = re.findall(rule, split_cell)
    if country_producer_text:
        info['country_producer'] = country_producer_text[0]

    return info

def get_cost_tax(td_tag: bs4.element.Tag) -> Dict:
    split_cell = ' '.join(td_tag.text.split())
    values = {
        'tax': None,
        'cost': None,
    }

    rule = r'Ставка НДС: \d+\,\d+|Ставка НДС: \d+\.\d+|Ставка НДС: \d+'
    rule += r'|Ставка НДС: Без НДС'
    tax = re.findall(rule, split_cell)
    # print(tax)
    if tax:
        tax_t = tax[0].replace('Ставка НДС: ', '')
        if tax_t == 'Без НДС':
            values['tax'] = 'Без НДС'
        else:
            values['tax'] = float(tax_t)
        split_cell = split_cell[:split_cell.find('Ставка НДС')]
        # split_cell = split_cell.replace(tax[0], '')

    cost_rule = '\d+\.\d+|\d+\,\d+|\d+'
    cost = re.findall(cost_rule, split_cell)
    if cost:
        cost = ''.join(cost).replace(',', '.')
        cost = float(cost)
        values['cost'] = cost

    return values
