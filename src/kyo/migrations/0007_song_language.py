# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-23 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyo', '0006_auto_20190723_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='language',
            field=models.CharField(default='english', max_length=255),
        ),
    ]
