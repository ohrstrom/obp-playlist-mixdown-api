# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 21:14
from __future__ import unicode_literals

from django.db import migrations, models
import mixdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('mixdown', '0007_playlist_target_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='content_hash',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='mixdown_file',
            field=models.FileField(blank=True, null=True, upload_to=mixdown.models.get_mixdown_upload_path),
        ),
    ]
