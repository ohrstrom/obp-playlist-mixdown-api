# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 07:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mixdown', '0009_remove_playlist_remote_absolute_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='target_duration',
            new_name='duration',
        ),
    ]
