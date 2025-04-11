from .common_info import read_common_info
from .product_info import read_product_info
from .penalty_info import check_penalty

'''
    Должны быть функции принимающие ответ от сайта: Response
    url_example = "https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=3352808136323000106"

    Парсинг "карточки контракта"
        ОБЩАЯ ИНФОРМАЦИЯ
        ПЛАТЕЖИ И ОБЪЕКТЫ ЗАКУПКИ
        ИСПОЛНЕНИЕ (РАСТОРЖЕНИЕ) КОНТРАКТА
        ВЛОЖЕНИЯ            - не трогаем
        ЖУРНАЛ ВЕРСИЙ       - не трогаем
        ЖУРНАЛ СОБЫТИЙ      - не трогаем
'''
