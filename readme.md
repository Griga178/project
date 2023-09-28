# Набор рандомных функций и проч. основанных на Django

## шаг 0 - создание каталогов "app"
  py -m django startproject app
  (в случае, когда django не прописан в path системы
  https://docs.djangoproject.com/en/4.2/ref/django-admin/
  )

###   запуск:
  app/manage.py runserver

###   стандартный url
  http://127.0.0.1:8000/

###   добавление приложения:
  app/manage.py startapp my_parser

## База данных (sqlite3)

### После каждого изменения:
  manage.py makemigrations
  manage.py migrate



## функкция 1 "парсер_0"
https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Generic_views
  вход: ссылка + теги

  выход: текст по ссылке и тегу

  есть форма для ввода ссылки
  есть форма для ввода тегов (3шт)

  ссылка при вводе сохраняется в БД
  теги при вводе сохраняются в БД

  есть таблица с историей парсинга:
  ссылка - дата - теги - результат

  функция повторить

  модули:
    requests
    beautifullsoup
