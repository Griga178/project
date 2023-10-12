from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

import re


# Create your models here.

class Domain(models.Model):

    name = models.TextField(help_text = "Введите домен", unique = True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/domains/%i/" % self.id

    class Meta:
        verbose_name_plural = 'Домены'

class Domain_setting(models.Model):
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE, verbose_name = 'Домен', null = True)

    content_choices = [
        ('price', 'Цена -> float'),
        ('name', 'Название -> str'),
        ('chars', 'Характеристики -> list'),
        ('other_str', 'прочее -> str'),
        ('other_list', 'прочее -> list'),
    ]
    content_type = models.CharField(verbose_name = "Тип содержимого", unique = False,
        choices = content_choices, max_length = 50)

    tag = models.TextField(verbose_name = "Имя тега", unique = False)
    attr = models.TextField(verbose_name = "Имя атрибута", unique = False)
    attr_val = models.TextField(verbose_name = "Значение атрибута", unique = False)

    def __str__(self):
        return f'{self.domain} - {self.content_type}'
    def get_absolute_url(self):
        return "/domain_settings/%i/" % self.id

    class Meta:
        verbose_name_plural = 'Настройки для парсинга'

class Link(models.Model):

    name = models.TextField(help_text = "Введите ссылку", unique = True)
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE, verbose_name = 'Домен', null = True)

    def __str__(self):
        return self.name

    def check_link(self):
        reg_set = r'^https://+\S+|http://+\S+'
        re_sults = re.findall(reg_set, self.name)
        if re_sults:
            return re_sults[0]
        else:
            return False

    def get_domain(self):
        domain_string = self.name.split('/')[2]
        return domain_string

    def clean(self):
        if not self.check_link():
            raise ValidationError(
                {'name': "Ссылка должа быть ссылкой!"})

    def get_absolute_url(self):
        return "/links/%i/" % self.id

    class Meta:
        verbose_name_plural = 'Ссылки'

class Parse_result(models.Model):

    link = models.ForeignKey(Link, on_delete = models.CASCADE, verbose_name = 'Ссылка', null = False)
    domain_setting = models.ForeignKey(Domain_setting, on_delete = models.CASCADE, verbose_name = 'Настройка', null = False)

    value = models.TextField(verbose_name = "Результат парсинга", unique = False)
    parse_date = models.DateTimeField(verbose_name = "Дата", auto_now_add = True, blank = True)

    class Meta:
        verbose_name_plural = 'Результаты парсинга'

    def __str__(self):
        return f'{self.parse_date.strftime("%H:%M %d.%m.%y")} - {self.domain_setting}: {self.value}'


@receiver(post_save, sender = Link)
def Domain_save(sender, instance, **kwargs):
    '''
        при добавлении ссылки создается связь с доменом,
        если нет домена создается новый
    '''
    domain_string = instance.get_domain()

    if not instance.domain:
        try:
            domain = Domain.objects.get(name = domain_string)
        except Domain.DoesNotExist:
            domain = Domain(name = domain_string)
            domain.save()
        instance.domain = domain
        instance.save()
