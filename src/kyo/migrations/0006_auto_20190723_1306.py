# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-23 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kyo', '0005_auto_20190723_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='song',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='words', to='kyo.Song'),
        ),
    ]
