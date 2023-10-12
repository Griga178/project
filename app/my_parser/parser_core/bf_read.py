'''
    чтение содержимого искомых тегов
'''
from .data_converter import string_to_float, clean_string
from bs4 import BeautifulSoup

def find_content_old(html_page, settings):

    bf_page = BeautifulSoup(html_page, 'html.parser')
    # bf_response = {}
    bf_response = []

    for set_up in settings:
        # print(set_up['tag'])
        dirty_content = bf_page.find(set_up['tag'], attrs = {set_up['attr']: set_up['attr_val']})
        if dirty_content != None:
            content = dirty_content.text
        else:
            content = None

        # bf_response[set_up['content_type']] = content
        bf_response.append({
            'content_type': set_up['content_type'],
            'content': content
            })

    return bf_response

def find_content(html_page, setting):

    bf_page = BeautifulSoup(html_page, 'html.parser')

    dirty_content = bf_page.find(setting.tag, attrs = {setting.attr: setting.attr_val})
    if dirty_content != None:
        if setting.content_type == 'price':
            cur_func = string_to_float
        elif setting.content_type == 'name':
            cur_func = clean_string
        content = cur_func(dirty_content.text)
    else:
        content = None

    return content
