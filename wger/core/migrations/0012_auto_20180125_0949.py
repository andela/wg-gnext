# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-01-25 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20180124_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='can_create_users',
            field=models.BooleanField(default=False),
        ),
    ]
