# from .main import *
# Parser_class = Parser_ver_2

from .test import *
Parser_class = Parser_ver_3

from .card_parsing import read_common_info
from .card_parsing import read_product_info
from .card_parsing import check_penalty
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import PendingRollbackError
'''
    Добавление функций к парсеру
    парсинг инфы из карточки контракта
'''
def read_product_page(self):
    pass

def parse_common_info(self, contruct_number: int):
    common_url = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html'
    pr_param = {
        'reestrNumber': contruct_number,
    }

    response = self.session.get(
        common_url,
        headers = self.headers,
        params = pr_param)

    if response.status_code == 200:
        common_info = read_common_info(response)
        # for key, val in common_info.items():
        #     print(key, ' - ', [val])

        return common_info
    elif response.status_code == 429:
        print('Status code 429 -> sleep and restart!')

        self.session.close()
        time.sleep(12)
        self.parse_common_info(contruct_number)

    else:
        print('response.status_code != 200 - string 34')
        print(response.status_code)
        return None

def parse_target_info(self, contruct_number: int, pageSize: int = 50):
    targets_url = f'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order-list.html'

    pr_param = {
        'reestrNumber': contruct_number,
        'pageSize': pageSize
    }

    response = self.session.get(
        targets_url,
        headers = self.headers,
        params = pr_param)

    if response.status_code == 200:
        # print(contruct_number)
        target_info = read_product_info(response)
        # for key, val in target_info.items():
        #     print(key, ' - ', [val])

        return target_info
    else:
        print(response.status_code)
        return None

def parse_penalty(self, contruct_number: int):
    process_url = f'https://zakupki.gov.ru/epz/contract/contractCard/process-info.html'
    pr_param = {
        'reestrNumber': contruct_number,
    }
    response = self.session.get(
        process_url,
        headers = self.headers,
        params = pr_param)
    if response.status_code == 200:
        common_info = check_penalty(response)
        # print(common_info)
        return common_info
        # for key, val in common_info.items():
        #     print(key, ' - ', [val])
    else:
        print(response.status_code)
        return None

def parse_products(self):
    '''
    Парсинг товаров из контрактов и
    прочей инфы (заказчик, штрафы)
    '''
    # НУЖНО ОТФИЛЬТРОВАТЬ УЖЕ ОТПАРСЕННЫЕ КОНТРАКТЫ
    # получение инфы из связи контракт - продукт
    # вызывает новое обращение к бд - очень долго
    # получаем номера отпарсенных контракты
    p_numbers = set(self.Product.query.with_entities(self.Product.contrant_card_id).all())
    # получаем номера всех контракты
    c_numbers = set(self.Contrant_card.query.with_entities(self.Contrant_card.number).all())
    # оставляем номера только тех, которые не парсили
    not_parsed_numbers_set = c_numbers - p_numbers
    # !!! ВОЗВРАЩАЕТ { (1780100227424000036,), (3890505754424000005,), ...}
    # print(len(not_parsed_numbers_set))

    # print(not_parsed_numbers_set)
    start_time = time.time()
    p_counter = 0
    product_counter_common = 0

    for contruct_number in not_parsed_numbers_set:

        p_counter += 1
        # парсим первую страницу с общей информацией
        try:
            common_info = self.parse_common_info(contruct_number[0])

        except Exception as e:
            print(f'\Common_info error - {contruct_number[0]}\n')
            # print(e.message)
            continue
        if common_info:
            if type(common_info['product_amount']) == int:
                product_amount = common_info['product_amount']
            else:
                product_amount = 50
        else:
            product_amount = 50
        # парсим страницу со списком товаров

        try:
            target_info = self.parse_target_info(contruct_number[0], product_amount)
        except Exception as e:
            print(f'\nProduct error - {contruct_number[0]}\n')
            # print(e.message)
            continue


        # парсим страницу с информацией по штрафам
        try:
            penalty_info = self.parse_penalty(contruct_number[0])
        except Exception as e:
            print(f'\nPenalty error - {contruct_number[0]}\n')
            # print(e.message)
            continue


        # Вносим информацию в бд
        try:
            print(common_info['provider_inn'])
            provider = self.db.session.query(self.Company).filter_by(inn = common_info['provider_inn']).one()
            provider_inn = provider.inn
        except NoResultFound:
            # self.db.session.rollback()
            if common_info['provider_inn']:
                provider = self.Company(
                    inn = common_info['provider_inn'],
                    name = common_info['provider'],
                )
                provider_inn = provider.inn
                self.db.session.add(provider)
                try:
                    self.db.session.commit()
                except OperationalError:
                    print('\nOperationalError: provider_appending', c_db.number, '\n\n')
                    self.db.session.rollback()
                    continue
                except PendingRollbackError:
                    self.db.session.rollback()
                    continue
            else:
                provider_inn = None
        except Exception as e:
            print('ERROR string 164:', e)
            # time.sleep(3)
            # print(self.session.__dir__())
            # self.session.close()
            # self.parse_products()
            # print('sleep 3 sec')
            # break
            continue

        c_db = self.db.session.query(self.Contrant_card).filter_by(number = contruct_number[0]).one()

        c_db = self.db.session.query(self.Contrant_card).filter_by(number = contruct_number[0]).one()
        c_db.price = common_info['price'] if not c_db.price else c_db.price
        c_db.customer = common_info['customer'] if not c_db.customer else c_db.customer

        c_db.update_date = datetime.strptime(common_info['update_date'], '%d.%m.%Y') if not c_db.update_date else c_db.update_date
        c_db.place_date = datetime.strptime(common_info['place_date'], '%d.%m.%Y') if not c_db.place_date else c_db.place_date
        c_db.execute_date = datetime.strptime(common_info['execute_date'], '%d.%m.%Y') if not c_db.execute_date else c_db.execute_date

        c_db.penalty = penalty_info['penalty_bool'] if not c_db.penalty else c_db.penalty

        c_db.provider_id = provider_inn
        # c_db.product_amount = common_info['product_amount'] if not c_db.product_amount else c_db.product_amount
        try:
            self.db.session.add(c_db)
            self.db.session.commit()
        except OperationalError:
            print('\nOperationalError: common_info', c_db.number, '\n')
            self.db.session.rollback()
            continue

        except PendingRollbackError:
            self.db.session.rollback()
            continue
        # print()

        product_counter = 0
        try:
            for prod in target_info['products']:
                prod['contrant_card_id'] = c_db.number
                # print(p_counter, prod)
                product_counter += 1
                product_counter_common += 1
                product_object = self.Product(**prod)
                self.db.session.add(product_object)

            self.db.session.commit()
            print(p_counter, product_counter, '<- - -', end = '\r')

            if p_counter % 10 == 0:
                time.sleep(4)
                # pass
        except OperationalError:
            print('\nOperationalError:', c_db.number, '\n')
            self.db.session.rollback()
        except Exception as e:
            print('\nOther ERROR  string 212\n:', c_db.number, '\n', )


        # if p_counter > 28344:
        #     cur_sec = round((time.time() - start_time), 2)
        #     print(f'Контракты: {p_counter}\nПродукты: {product_counter_common}')
        #     print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. == {cur_sec} сек.)')
        #     break
    else:
        cur_sec = round((time.time() - start_time), 2)
        print(f'Контракты: {p_counter}\nПродукты: {product_counter_common}')
        print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')




Parser_class.parse_products = parse_products
Parser_class.parse_common_info = parse_common_info
Parser_class.parse_target_info = parse_target_info
Parser_class.parse_penalty = parse_penalty
