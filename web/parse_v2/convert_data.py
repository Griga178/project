from re import findall
from datetime import datetime, timedelta

def string_to_float(string):
    try:
        reg_set = r'\d|\.|\,'
        results = findall(reg_set, string)
        result = ''.join(results).replace(',', '.')
        number = float(result)
        return number
    except:
        return None

def string_to_int(string):
    reg_set = r'\d'
    results = findall(reg_set, string)
    result = ''.join(results)
    number = int(result)
    return number

def string_to_datetime(string_value):

    '''
        преобразует строку времени с разными разделителями в datetime
    '''
    # делим строку на числа ["01", "01", "2020", '19', '22', 00]
    try:
        string_numbers = findall(r'\d+', string_value)
        datetime_str_format = '%d.%m.%Y'
        string_date = ".".join(string_numbers[0:3])
        if len(string_numbers) > 3:
            datetime_str_format += " %H"
            string_date += f' {string_numbers[3]}'
        if len(string_numbers) > 4:
            datetime_str_format += ":%M"
            string_date += f':{string_numbers[4]}'
        if len(string_numbers) > 5:
            datetime_str_format += ":%S"
            string_date += f':{string_numbers[5]}'
        datetime_object = datetime.strptime(string_date, datetime_str_format)
        return datetime_object
    except:
        return None

def clean_string(string):
    rvar = r'\w+'
    results = findall(rvar, string)
    result = ' '.join(results)
    return result

def form_string_to_datetime(string_value):

    '''
        преобразует строку времени с разными разделителями в datetime
    '''
    # делим строку на числа ["01", "01", "2020", '19', '22', 00]

    string_numbers = findall(r'\d+', string_value)
    datetime_str_format = '%Y-%m-%d'
    string_date = "-".join(string_numbers[0:3])

    datetime_object = datetime.strptime(string_date, datetime_str_format)
    return datetime_object
