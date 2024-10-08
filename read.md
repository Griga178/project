Парсим контракты с сайта zakupki.gov.ru

в app3 (flask-е) requests - парсер (без selenium)
фильтры в заголовках

NOt actual settings.py
  Выбор даты
  Скачать актуальный драйвер

NOt actual app.py
  Скачиваем номера контрактов

NOt actual get_card_info.py
  Скачиваем инфу по закупленным товарам в контракте

NOt actual app2.py
  поиск совпадений по:
    ОКПД2 + ЦЕНА (+/- 30%)
    НАЗВАНИЕ + ЦЕНА (+/- 30%)


4 app3.py
  веб интерфес с поиском по БД(flask)

Процесс парсинга номеров:
  составления списка дат для поиска
  выставление фильтров на сайте
  проход по страницам пока они не закончатся

Процесс парсинга инф-и из карточки:
  выгрузка контрактов из БД, на которые не ссылаются товары (не парсились)




Миграции Бд

установка:
pip install alembic
инит в папку "migration":
py -m alembic init migration

указываем путь до БД: alembic.ini
sqlalchemy.url = sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/zakupki.db

импортируем + подключаем Метаданные от sqlalchemy: migration/env.py
from db import *
target_metadata = Base.metadata

Создаем версию БД
py -m alembic revision --autogenerate -m 'initial'

внесение изменений
1 вносим изменения в модель (tables.py)
2 создаем автоматическую миграцию:
py -m alembic revision --autogenerate  -m "comment"

4 запуск
py -m alembic upgrade 911...
...вносятся изменения в sql таблице
