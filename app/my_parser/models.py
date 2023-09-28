from django.db import models

# Create your models here.
class Link(models.Model):
    """
    Ссылки
    """
    name = models.TextField(help_text = "Введите ссылку", unique = True)

    def __str__(self):
        return self.name
