from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

import re


# Create your models here.
class Link(models.Model):

    name = models.TextField(help_text = "Введите ссылку", unique = True)
    # domain = models.ForeignKey(Domain, verbose_name = 'Домен')

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

@receiver(post_save, sender = Link)
def Link_save(sender, instance, **kwargs):
    domain_string = instance.get_domain()
    # domain_id = 
    print('1', instance.id, domain_string, instance.name)

# class Domain(models.Model):
#
#     name = models.TextField(help_text = "Введите домен", unique = True)
