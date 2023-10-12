import re


def string_to_float(string):
    reg_set = r'\d|\.|\,'
    results = re.findall(reg_set, string)
    result = ''.join(results).replace(',', '.')
    number = float(result)
    return number

def clean_string(string):
    rvar = r'\w+'
    results = re.findall(rvar, string)
    result = ' '.join(results)
    return result
