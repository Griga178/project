from requests import Response
from typing import Dict
from bs4 import BeautifulSoup

import re
def read_common_info(response: Response) -> Dict:
    '''
        Сбор информации со страницы:
        https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=2470000125421000431
        price
        date, execute_date, place_date, update_date
        customer, customer_short, customer_inn,
        provider, provider_inn,
        product_amount

    '''
    response_kw = {
        'is_success': False
    }

    soup = BeautifulSoup(response.text, 'html.parser')
    response_kw['title'] = soup.title.text
    if soup.title.text == 'Карточка контракта':

        # Первый общий блок
        main_info_table = soup.find_all('div', {"class": "sectionMainInfo"})

        # Находим количество закупленных товаров
        target_span_name = main_info_table[0].find('div', string = 'Объекты закупки')
        target_text = target_span_name.parent.find_all('div')[1].text
        rule = r'Посмотреть все \(\d+\)'
        target_string = re.findall(rule, target_text)
        if target_string:
            response_kw['product_amount'] = int(re.findall('\d+', target_string[0])[0])
        else:
            response_kw['product_amount'] = 1

        # Читаем разные даты контрактов
        date_rows = [
            ('price', 'Цена контракта'),
            ('date', 'Заключение контракта'),
            ('execute_date', 'Срок исполнения'),
            ('place_date', 'Размещен контракт в реестре контрактов'),
            ('update_date', 'Обновлен контракт в реестре контрактов'),
        ]
        for key, span_string in date_rows:
            try:
                span_name = main_info_table[1].find('span', string = span_string)
                if key == 'price':
                    span_date = span_name.parent.find_all('span')[1].text
                    str_price = ''.join(span_date.split())
                    response_kw[key] = float(str_price.replace('₽', '').replace(',', '.'))
                else:
                    span_date = span_name.parent.find_all('span')[1].text
                    response_kw[key] = span_date.split()[0]
            except:
                response_kw[key] = None

        h2_tag = soup.find('h2', string = 'Информация о заказчике')
        common_info = h2_tag.parent

        # Читаем разные инфу о заказчике
        info_rows = [
            ('customer', 'Полное наименование заказчика'),
            ('customer_short', 'Сокращенное наименование заказчика'),
            ('customer_inn', 'ИНН'),
            ]

        for key, span_string in info_rows:
            try:
                span_name = common_info.find('span', string = span_string)
                if key == 'customer':
                    # Тут ссылка, убраем отступы
                    span_date = span_name.parent.find_all('span')[1].text
                    span_date = ' '.join(span_date.split())
                else:
                    span_date = span_name.parent.find_all('span')[1].text
                response_kw[key] = span_date
            except:
                response_kw[key] = None

        # Читаем разные инфу о Поставщике
        provider_block = soup.find('div', {'class': 'participantsInnerHtml'})
        provider_cell = provider_block.table.tbody.tr.td
        provider_name = provider_cell.find(text = True, recursive = False)
        response_kw['provider'] = ' '.join(provider_name.split())
        inn_span = provider_cell.find('span', string = 'ИНН:')
        response_kw['provider_inn'] = inn_span.parent.find_all('span')[1].text

        response_kw['is_success'] = True
        return response_kw
    else:
        return response_kw
