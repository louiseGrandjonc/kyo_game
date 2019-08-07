# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-05 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kyo', '0007_song_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='words', to='kyo.Artist'),
        ),
    ]
