# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-26 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bbus', '0003_remove_bbu_load'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbu',
            name='freC_DL',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bbu',
            name='freC_UL',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]