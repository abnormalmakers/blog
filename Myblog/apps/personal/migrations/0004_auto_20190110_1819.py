# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-10 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_auto_20190110_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_del',
            field=models.BooleanField(default=False),
        ),
    ]