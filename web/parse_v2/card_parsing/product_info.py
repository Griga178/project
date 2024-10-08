from requests import Response, get
from typing import Dict
from bs4 import BeautifulSoup
import re

from .product_info_addition import *

def read_product_info(response: Response) -> Dict:
    '''
        Сбор информации со страницы с закупленными товарами:
        https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order-list.html?reestrNumber=3310900451323000020&pageSize=1
        contract_price, product_ammount
        products: [
            name:
            price:
            ...
        ]


    '''
    response_kw = {
        'is_success': False,
        'products': []
    }
    # проверка, в таблице находятся все продукты?
    targets = re.findall(r'pageSize\=\d+', response.url)
    target_product_ammount = int(re.findall(r'\d+', targets[0])[0])

    soup = BeautifulSoup(response.text, 'html.parser')
    product_table = soup.find('table')

    footer = product_table.tfoot.find_all('td')
    product_ammount = int(re.findall(r'\d+', footer[0].text)[0])
    try:
        contract_price = float(''.join(footer[1].text.split()).replace(',', '.'))
    except:
        contract_price = None

    if product_ammount > target_product_ammount:
        # Запросили меньше чем есть по факту
        new_url = response.url.replace(f'pageSize={target_product_ammount}', f'pageSize={product_ammount}')
        response = get(new_url, headers = response.request.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        product_table = soup.find('table')

    response_kw['product_ammount'] = product_ammount
    response_kw['contract_price'] = contract_price

    table_rows = product_table.tbody.find_all('tr', {'class': 'tableBlock__row', 'id': None}, recursive = False)
    
    for table_row in table_rows[:]:
        product = {}
        cells = table_row.find_all('td')

        # Имя возм: страна + ктру + окпд2
        product = product | get_product_name_country(cells[1])
        # ктру + окпд2
        product = product | get_ktru_okpd_2(cells[2])
        # Тип объекта закупки
        product = product | get_product_type(cells[3])
        # Количество
        product = product | get_quantity_measure(cells[4])
        # Цена
        product = product | get_price(cells[5])
        # Страна
        if not product['country_producer']:
            product = product | get_country_producer(cells[6])
        # Сумма + НДС
        product = product | get_cost_tax(cells[7])
        response_kw['products'].append(product)

    # for el in response_kw['products']:
        # print(el)


    response_kw['is_success'] = True
    return response_kw
