# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-10 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_auto_20190103_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_del',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(default='2019-01-10'),
        ),
        migrations.AlterField(
            model_name='article_tag',
            name='article',
            field=models.ManyToManyField(to='personal.Article'),
        ),
    ]
