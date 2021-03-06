# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixdown', '0003_auto_20170524_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='remote_uri',
            field=models.URLField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Initialized'), (1, 'Pending'), (2, 'Processing'), (3, 'Delivered'), (99, 'Seen')], db_index=True, default=1, verbose_name='Status'),
        ),
    ]
