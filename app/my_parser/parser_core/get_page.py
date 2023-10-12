'''
    Получение "кода страницы через requests"
'''

import requests

def get_page(link):
    return requests.get(link).text
