# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-11 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tagview',
            options={'ordering': ['-count', 'tag']},
        ),
    ]