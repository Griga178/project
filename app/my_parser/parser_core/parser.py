import requests
from bs4 import BeautifulSoup

class Parser():
    '''
    Набор функций парсинга
    '''

    def get_html(link: str) -> str:
        '''
        '''
        return requests.get(link).text

    def find_value(html_page: str, settings: dict) -> str:
        '''
        '''
        how = settings.get('how')
        if how == 'requests-html':
            soup = BeautifulSoup(html_page, 'html.parser')
            value = soup.find(setting['tag'], attrs = {setting['attribute']: setting['value']})
        elif how == 'selenium':
            '''
                запуск драйвера -> поиск по тегу
            '''
        else:
            return ' i do not how parse it'


        return 'value'
