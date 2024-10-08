import requests

from .bs_funcs import *
from .db_func import *
from .convert_data import *
from sqlalchemy import desc

class Parser_ver_2():
    get_last_conrtact_date = get_last_conrtact_date
    get_today = get_today
    insert_new = insert_new
    def __init__(self, **kwargs):
        self.app = kwargs['app']
        self.db = kwargs['db']
        # self.db_api = kwargs['db_api']
        self.Company = kwargs['Company']
        self.Contrant_card = kwargs['Contrant_card']
        self.Product = kwargs['Product']

        self.url = 'https://zakupki.gov.ru/epz/contract/search/results.html'
        self.pr_card_url = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            }
        self.params = {
            'morphology': 'on',
            'search-filter': 'Цене', # 'Цене' 'Дате размещения'
            'fz44': 'on',
            'contractStageList_1': 'on',
            'contractStageList': 1,
            'contractCurrencyID': -1,
            'budgetLevelsIdNameHidden': '{}',
            # 'contractDateFrom': '30.12.2023',
            # 'contractDateTo': '02.02.2024',
            'sortBy': 'PRICE', #PRICE UPDATE_DATE
            'pageNumber': 1, # '1'
            'sortDirection': 'false',
            'recordsPerPage': '_50', #_10, _20, _50
            'showLotsInfoHidden': 'false',
            'customerPlace': 5277347,
            'customerPlaceCodes': 78000000000
            }

        self.app_status = 0

        self.counter = 0
        self.parse_progress = 0
        self.days_amount = 0
        self.session = requests.Session()
        self.query_attemps_q = 0
        self.report = {}
        self.date_from = self.get_last_conrtact_date()
        self.date_to = self.get_today()
        self.filter_date_from = False
        self.filter_date_to = False
        self.price_filter = False

        response = self.session.get(
            self.url,
            headers = self.headers)

        if response.status_code != 200:
            print(response)

            return {'error': 1,
            'message': f'Ошибка {response.status_code} при запуске'}
        else:
            self.status_code = response.status_code

    def get_query(self):
        response = self.session.get(
            self.url,
            headers = self.headers,
            params = self.params)
        return response

    def set_dates(self, *args, **kwargs):
        if len(args) == 1:
            self.date_from = string_to_datetime(args[0])
        elif len(args) == 2:
            self.date_from = string_to_datetime(args[0])
            self.date_to = string_to_datetime(args[1])
        else:

            if kwargs.get('date_from') or kwargs.get('date_to'):
                self.date_from = form_string_to_datetime(kwargs.get('date_from')) if kwargs.get('date_from') else False
                self.date_to = form_string_to_datetime(kwargs.get('date_to')) if kwargs.get('date_to') else False
            else:
                pass
                print(f'Не вставлены даты a:{args} k:{kwargs}')

        if self.date_to == False:
            self.date_to = self.get_today()

        if self.date_from == False:
            self.date_from = self.get_last_conrtact_date()


        self.filter_date_from = self.date_from
        # else:
        #     if last_datetime > self.date_from:
        #         self.date_from = last_datetime

    def set_dates_query(self):
        self.params['contractDateFrom'] = self.filter_date_from.strftime('%d.%m.%Y')
        self.params['contractDateTo'] = self.filter_date_to.strftime('%d.%m.%Y')

    def parse_contract_numbers(self):
        self.app_status = 1
        self.days_amount = (self.date_to - self.date_from).days
        days_step = 5
        # настраиваем запрос
        self.filter_date_to = self.filter_date_from + timedelta(days = days_step)
        self.set_dates_query()
        print('Запуск парсера')
        while self.filter_date_from < self.date_to and self.app_status == 1:
            self.parse_progress = round((1 - (self.date_to - self.filter_date_from).days / self.days_amount) * 100)
            # print(self.parse_progress, self.days_amount)
            response = self.get_query()
            if response.status_code != 200:
                print(f'ОШИБКА ПРИ ПЕРВОМ ЗАПРОСЕ: {response.status_code} ({self.query_attemps_q})')
                if self.query_attemps_q > 10:
                    self.report['message'] = f'>10 попыток запроса {response.status_code}'
                    self.report.update(self.params)
                    print(self.report)
                    break
                time.sleep(1)
                self.query_attemps_q += 1
                continue
            else:
                self.query_attemps_q = 0
            # проверяем количество контрактов
            contract_amount = get_contract_amount(response)
            # print(self.params['contractDateFrom'], '-', self.params['contractDateTo'])
            # print('Нашлось контрактов:', contract_amount)

            if contract_amount == 0:
                self.filter_date_from += timedelta(days = 1)
                self.filter_date_to = self.filter_date_from + timedelta(days = days_step)
                self.set_dates_query()
                continue
            elif contract_amount < 1000:
                page_amount = get_page_amount(contract_amount)
                self.price_filter = False
            else:

                if self.filter_date_from == self.filter_date_to:
                    page_amount = 20
                    self.price_filter = True
                else:
                    self.filter_date_to = self.filter_date_to - timedelta(days = 1)
                    self.set_dates_query()
                    continue

            # сохраняем контракты - перелистываем
            contrant_cards = []
            for i in range(page_amount):
                # print(f'скачиваем контракты с листа № {self.params["pageNumber"]}')
                contrant_cards += get_contract_numbers(response)
                self.counter += len(contrant_cards)
                # print('перелистываем')
                self.params['pageNumber'] += 1

                response = self.get_query()
                if response.status_code != 200:
                    print(f'ОШИБКА ПРИ ПЕРЕЛИСТЫВАНИИ: {response.status_code} ({self.query_attemps_q})')
                    if self.query_attemps_q > 10:
                        self.query_attemps_q = 0
                        self.report['message'] = f'>10 попыток запроса ПЕРЕЛИСТЫВАНИЯ {response.status_code}'
                        self.report.update(self.params)
                        print(self.report)
                        if contrant_cards:
                            self.insert_new(contrant_cards)
                            print(f'Контракты сохранили {len(contrant_cards)}')
                        break
                    time.sleep(1)
                    self.query_attemps_q += 1
                    continue
                else:
                    self.query_attemps_q = 0

            else:
                self.params['pageNumber'] = 1
                self.insert_new(contrant_cards)
                print(f'Контракты сохранили {len(contrant_cards)}')



            if self.price_filter:
                # максимальная цена отпарсенного контракта
                self.params['contractPriceFrom'] = 1000000
            else:
                self.filter_date_from = self.filter_date_to + timedelta(days = 1)
                self.filter_date_to += timedelta(days = days_step)
                self.set_dates_query()
                if self.params.get('contractPriceFrom'):
                    del self.params['contractPriceFrom']
        else:
            self.app_status = 11
            self.parse_progress = 100
            # self.params['pageNumber'] = 1
            if self.params.get('contractPriceFrom'):
                del self.params['contractPriceFrom']
            # if self.params.get('contractDateFrom'):
            #     del self.params['contractDateFrom']
            # if self.params.get('contractDateTo'):
            #     del self.params['contractDateTo']

    def refresh_app(self):
        self.parse_progress = 0
        self.counter = 0
        self.date_from = self.get_last_conrtact_date()
        self.date_to = self.get_today()

    def get_info(self):
        return {
            'app_status': self.app_status,
            'counter': self.counter,
            'parse_progress': self.parse_progress,
            'start_date': self.date_from.strftime("%Y-%m-%d"),
            'end_date': self.date_to.strftime("%Y-%m-%d"),
            'parse_date_from': self.filter_date_from.strftime("%Y-%m-%d") if self.filter_date_from else None,
            'parse_date_to': self.filter_date_to,
        }

    def get_sum_info(self):
        # eca = self.Contrant_card.query.filter(self.Contrant_card.update_date == None).count()
        try:
            fcd = self.Contrant_card.query.order_by(self.Contrant_card.date).first().date.strftime("%Y-%m-%d")
            lcd = self.Contrant_card.query.order_by(desc(self.Contrant_card.date)).first().date.strftime("%Y-%m-%d")
            lud = self.Contrant_card.query.order_by(desc(self.Contrant_card.update_date)).first().date.strftime("%Y-%m-%d")
            c_numbers = set(self.Contrant_card.query.with_entities(self.Contrant_card.number).all())
            p_numbers = set(self.Product.query.with_entities(self.Product.contrant_card_id).all())
            eca = len(c_numbers - p_numbers)
        except:
            fcd = None
            lcd = None
            lud = None
            eca = None

        response = {
            'last_update_date': lud,
            'contract_amount': self.Contrant_card.query.count(),
            'empty_contract_amount': eca,
            'product_amount': self.Product.query.count(),
            'first_contract_date': fcd,
            'last_contract_date': lcd,
            'today_date': self.date_to.strftime("%Y-%m-%d"),
        }
        response.update(self.get_info())
        return response
