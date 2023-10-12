# Generated by Django 3.2.16 on 2023-10-10 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_parser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Введите домен', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='domain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_parser.domain', verbose_name='Домен'),
        ),
    ]
