# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-23 08:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('nvfis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nvfi',
            name='type',
        ),
    ]
