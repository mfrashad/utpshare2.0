# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-24 09:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_time_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='time_updated',
        ),
    ]
