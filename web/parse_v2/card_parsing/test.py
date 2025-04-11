import requests
from common_info import read_common_info
# from product_info import read_product_info
from penalty_info import check_penalty

reestrNumberS = [
    # 3310900451323000020,
    # 2771515296723000026,
    # 2470000125421000431,
    # 2470000125421000532,
    # 3482603760423000031,
    # 2780231180722000024,
    # 2780400987022000071,
    # 2781015837323000040,
    1783000258223000134, # С ошибкой!!! other error
    1784232871924000014, # С ошибкой common_info error!!!
    1783000258223000132, # С ошибкой!!! other error
    2780547060422000018, # Product error
]



target_of_order_url = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html'
# без стилей


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for reestrNumber in reestrNumberS[:]:
    # получаем общую инфу с первой страницы

    common_info_url = f'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber={reestrNumber}'
    # response = requests.get(common_info_url, headers = headers)
    # print('\nОбщая инфа')
    # if response.status_code == 200:
    #     common_info = read_common_info(response)
    #     for key, val in common_info.items():
    #         print(key, ' - ', [val])
    # else:
    #     print(response.status_code)

    # скачиваем закупленные объекты
    pageSize = 148
    # reestrNumber = 3234901331924000087
    # pageSize = 13
    # reestrNumber = 2780231180722000024
    targets_url = f'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order-list.html?reestrNumber={reestrNumber}&pageSize={pageSize}'
    response = requests.get(targets_url, headers = headers)
    print('\nЗакупленные товары:')
    if response.status_code == 200:
        common_info = read_product_info(response)
        for key, val in common_info.items():
            print(key, ' - ', [val])
    else:
        print(response.status_code)

    # смотрим штрафы

    process_url = f'https://zakupki.gov.ru/epz/contract/contractCard/process-info.html?reestrNumber={reestrNumber}'
    response = requests.get(process_url, headers = headers)
    if response.status_code == 200:
        common_info = check_penalty(response)
        print(common_info)
        # for key, val in common_info.items():
        #     print(key, ' - ', [val])
    else:
        print(response.status_code)
