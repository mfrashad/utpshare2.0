# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-23 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='order',
        ),
        migrations.AddField(
            model_name='sale',
            name='order',
            field=models.ManyToManyField(to='orders.Order'),
        ),
    ]
