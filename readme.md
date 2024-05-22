# Набор функций и проч. с интерфейсом на Django

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
app/settings.py DATABASES

### После каждого изменения:
  manage.py makemigrations
  manage.py migrate


## Класс "Парсер"

### Функции:
#### Работа с ссылкой
##### Добавить новую: str -> sql_object
##### Показать все: None -> List[sql_object]
##### Изменить по имени: str_old, str_new -> sql_object
##### Удалить по имени: str -> None

#### Работа со связями ссылкки
##### Определить домен: sql_object -> str
##### Определить создать новый домен

#### Работа настройками домена (crud)

#### Функции парсинга
##### request.get -> json
##### request -> html
##### selenium -> html

### База данных:
#### "Ссылка"
##### id
##### Имя
##### id домена (FK)

#### "Домен"
##### id
##### Имя

#### "Настройка"
##### id
##### id домена (FK)
##### Название
##### настройка: json_dict (
#####             how: "requests-html"|"requests.get"|"selenium"
#####             where: "by_tag_in_html"|"by_keys_in_http_resp"|"etc."
#####             tag, attribute, value,
#####             resp_keys)


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
