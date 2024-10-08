# Даты поиска контрактов
START_DATE = '30/05/2022'
# END_DATE = False # default = .now()
END_DATE = '01/01/2023' # default = .now()

# период, устанавливаемый в фильтре, на сайте
# количество дней в 1 запросе (если контрактов за период будет больше 1000),
# то период будет уменьшен
DAYS_STEP = 5 # ИСКАТЬ КОНТРАКТЫ ЗА X ДНЕЙ

# Путь до актуального драйвера для "Яндекса"
selenium_driver = '../yandexdriver.exe'

# Имя и место хранение SQL Базы данных
SQL_FILE_NAME = 'zakupki.db'
DATA_BASE_PATH = f'sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/{SQL_FILE_NAME}'


def get_last_conrtact():
    '''
        последний скачанный контракт
        ЧТО БЫ УСТАНОВИТЬ ДАТУ СТАРТА
        = ПОСЛЕДНЕЕ - 5 ДНЕЙ
    '''
    from database import Data_base_API
    DB_API = Data_base_API(DATA_BASE_PATH)

    all_contracts = DB_API.contrant_cards.select()
    all_contracts.sort(key = lambda x: x.date)
    print('Всего контрактов:', len(all_contracts))
    print('Всего контрактов:', all_contracts[-1])

# get_last_conrtact()
