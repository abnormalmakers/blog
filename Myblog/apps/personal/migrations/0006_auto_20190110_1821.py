# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-10 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0005_auto_20190110_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_del',
            field=models.BooleanField(default=False),
        ),
    ]
