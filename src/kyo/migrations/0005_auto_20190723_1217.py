# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-23 12:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kyo', '0004_auto_20190723_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordlyrics',
            name='album',
        ),
        migrations.RemoveField(
            model_name='wordlyrics',
            name='lyrics',
        ),
        migrations.RemoveField(
            model_name='wordlyrics',
            name='song',
        ),
        migrations.RemoveField(
            model_name='wordlyrics',
            name='word',
        ),
        migrations.RenameField(
            model_name='word',
            old_name='number_of_occurences',
            new_name='position',
        ),
        migrations.RemoveField(
            model_name='word',
            name='lyrics',
        ),
        migrations.AddField(
            model_name='word',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kyo.Album'),
        ),
        migrations.AddField(
            model_name='word',
            name='song',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kyo.Song'),
        ),
        migrations.DeleteModel(
            name='WordLyrics',
        ),
    ]