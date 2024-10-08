from requests import Response
from typing import Dict
from bs4 import BeautifulSoup

def check_penalty(response: Response = 0) -> Dict:
    kw = {}
    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        # table = soup.find('table', {'class': 'blockInfo__table '})
        table = soup.find('table')
        # print(table.prettify())
        target_row = table.find_all('tr')[1]
        # print(target_row.prettify())
        target_cell = target_row.find_all('td')[5].text
        answer = ''.join(target_cell.split())
        kw['penalty'] = answer
        if answer == 'Да':
            kw['penalty_bool'] = True
        elif answer == 'Нет':
            kw['penalty_bool'] = False
        else:
            kw['penalty_bool'] = None
    except:
        kw['penalty'] = None
        kw['penalty_bool'] = None

    return kw
