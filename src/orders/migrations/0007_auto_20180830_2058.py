# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-30 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20180830_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='address',
            field=models.CharField(default='utp', max_length=120),
        ),
    ]