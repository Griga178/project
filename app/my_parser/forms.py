# https://django.fun/ru/articles/tutorials/dinamicheskoe-dobavlenie-form-v-django-s-pomoshyu-naborov-form-i-javascript/

from django import forms
from .models import Link

# class LinkForm(forms.Form):
#     name = form.TextField(help_text = "Введите ссылку")

# Создаем форму для ввода экземляра (ссылок)
# с возможность ввести несколько ссылок
LinkFormSet = forms.modelformset_factory(
    Link, fields = ("name",), extra = 1
)

# автоматом заполнить 2 таблицы
# https://qna.habr.com/q/1101852
# @receiver
# https://djangodoc.ru/3.2/topics/signals/
