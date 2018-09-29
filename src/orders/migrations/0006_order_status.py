# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-28 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20180927_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('completed', 'Completed')], default='created', max_length=30),
        ),
    ]
