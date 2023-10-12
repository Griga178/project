# Generated by Django 3.2.16 on 2023-10-12 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_parser', '0004_auto_20231010_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain_setting',
            name='content_type',
            field=models.CharField(choices=[('price', 'Цена -> float'), ('name', 'Название -> str'), ('chars', 'Характеристики -> list'), ('other_str', 'прочее -> str'), ('other_list', 'прочее -> list')], max_length=50, verbose_name='Тип содержимого'),
        ),
        migrations.CreateModel(
            name='Parse_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(verbose_name='Результат парсинга')),
                ('parse_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('domain_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_parser.domain_setting', verbose_name='Настройка')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_parser.link', verbose_name='Ссылка')),
            ],
            options={
                'verbose_name_plural': 'Результаты парсинга',
            },
        ),
    ]