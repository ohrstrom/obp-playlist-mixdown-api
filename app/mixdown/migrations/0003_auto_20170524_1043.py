# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 10:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mixdown', '0002_auto_20170524_1021'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mixdown',
            new_name='Playlist',
        ),
    ]
