# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-04 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('name', 'album')]),
        ),
    ]
